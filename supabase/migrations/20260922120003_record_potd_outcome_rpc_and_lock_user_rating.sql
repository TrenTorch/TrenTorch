-- The one and only way profiles.user_rating ever changes. Computes the
-- Elo-style delta itself (potd-rating-system-spec.md §2) from a
-- server-looked-up difficulty/anchor, not from anything the client sends --
-- a client that could pass its own delta, difficulty, or rating_before
-- could set its own rating to whatever it wants, which given the real
-- interview referral this rating gates (§7) is not an acceptable surface.
--
-- Idempotent per (user_id, question_id) via rating_event's unique
-- constraint: a repeat call (e.g. the lazy day-end settlement check running
-- again on a later visit) is a no-op that returns the already-recorded
-- result, satisfying §5.1 (one rating event per problem, ever).
create or replace function public.record_potd_outcome(p_question_id text, p_outcome text)
returns table (rating_after integer, delta integer, already_recorded boolean)
language plpgsql
security definer
set search_path = public
as $$
declare
  v_user_id uuid := auth.uid();
  v_potd_date date;
  v_difficulty text;
  v_anchor integer;
  v_rating_before integer;
  v_e double precision;
  v_delta integer;
  v_rating_after integer;
  v_existing record;
begin
  if v_user_id is null then
    raise exception 'record_potd_outcome requires an authenticated user';
  end if;

  if p_outcome not in ('solved', 'failed') then
    raise exception 'invalid outcome: %', p_outcome;
  end if;

  -- Difficulty and date come from the schedule, never from the caller --
  -- see potd_schedule's migration for why.
  select potd_date, difficulty into v_potd_date, v_difficulty
  from public.potd_schedule
  where question_id = p_question_id;

  if v_potd_date is null then
    raise exception '% is not a Problem of the Day', p_question_id;
  end if;

  select re.rating_after, re.delta into v_existing
  from public.rating_event re
  where re.user_id = v_user_id and re.question_id = p_question_id;

  if found then
    return query select v_existing.rating_after, v_existing.delta, true;
    return;
  end if;

  v_anchor := case v_difficulty
    when 'easy' then 550
    when 'medium' then 850
    when 'hard' then 1250
    when 'advanced' then 1850
  end;

  -- Row lock: two concurrent submits for the same user (unlikely, but this
  -- is the one place a race could double-apply a delta) serialize here.
  select user_rating into v_rating_before
  from public.profiles
  where id = v_user_id
  for update;

  if v_rating_before is null then
    raise exception 'no profile found for %', v_user_id;
  end if;

  -- E = 1 / (1 + 10^((anchor - rating_before) / 400)) -- spec §2.
  v_e := 1.0 / (1.0 + power(10.0, (v_anchor - v_rating_before) / 400.0));

  if p_outcome = 'solved' then
    -- gain = round(K_gain * (1 - E)), K_gain = 100.
    v_delta := round(100 * (1 - v_e))::integer;
    v_rating_after := v_rating_before + v_delta;
  else
    -- loss = round(K_loss * E), K_loss = 20, floored at 400 (spec §5.2).
    v_delta := -round(20 * v_e)::integer;
    v_rating_after := greatest(400, v_rating_before + v_delta);
    -- Recompute delta from the clamped result so the audit log's delta
    -- always matches the rating's actual movement, even when the floor
    -- clipped it (e.g. a raw -13 next to a rating_before of 405 should log
    -- delta = -5, not -13).
    v_delta := v_rating_after - v_rating_before;
  end if;

  insert into public.rating_event (
    user_id, question_id, potd_date, difficulty, anchor_rating,
    rating_before, expected_e, outcome, delta, rating_after
  ) values (
    v_user_id, p_question_id, v_potd_date, v_difficulty, v_anchor,
    v_rating_before, v_e, p_outcome, v_delta, v_rating_after
  );

  update public.profiles set user_rating = v_rating_after where id = v_user_id;

  return query select v_rating_after, v_delta, false;
end;
$$;

-- Same PUBLIC-pseudo-role trap the earlier handle_new_user migrations
-- fixed: Postgres grants EXECUTE on new functions to PUBLIC by default,
-- which anon/authenticated inherit regardless of any per-role grant below.
revoke execute on function public.record_potd_outcome(text, text) from public;
grant execute on function public.record_potd_outcome(text, text) to authenticated;

-- Close the direct-write hole: today's "Users can update their own
-- profile" policy has a USING clause but no column restriction, so an
-- authenticated client could otherwise UPDATE profiles SET user_rating =
-- anything on their own row via the plain REST API, bypassing this
-- function (and its formula, floor, and audit log) entirely. Revoking
-- UPDATE on just this column leaves display_name/avatar_url updatable as
-- before; only a SECURITY DEFINER function (which runs as the table owner,
-- unaffected by this grant) can still move user_rating.
revoke update (user_rating) on public.profiles from authenticated, anon;
