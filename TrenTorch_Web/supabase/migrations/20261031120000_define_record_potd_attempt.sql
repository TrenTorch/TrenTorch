-- record_potd_attempt() was created by hand in the production database and
-- never had a migration, so a fresh or drifted environment had no definition
-- to reproduce or audit. The rating guard (guard_potd_rating_event) reads
-- potd_attempts.solved / solved_at, so those columns are part of the contract.
--
-- Semantics: one row per (user, POTD question). first_attempted_at is set on
-- the first submit and never moves; solved only ever flips false -> true and
-- solved_at records that first solve, so a later failed submit cannot undo a
-- solve and a retry of the same submit is a no-op.
alter table public.potd_attempts
  add column if not exists solved boolean not null default false,
  add column if not exists solved_at timestamptz,
  add column if not exists tests_passed integer,
  add column if not exists tests_total integer;

create or replace function public.record_potd_attempt(
  p_question_id text,
  p_tests_passed integer,
  p_tests_total integer,
  p_all_passed boolean
)
returns void
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_user_id uuid := auth.uid();
begin
  if v_user_id is null then
    raise exception 'record_potd_attempt requires an authenticated user'
      using errcode = '28000';
  end if;

  -- Same trust boundary as record_potd_outcome: only scheduled POTDs count.
  if not exists (
    select 1 from public.potd_schedule s where s.question_id = p_question_id
  ) then
    raise exception 'potd_attempt_unscheduled_question'
      using errcode = 'check_violation';
  end if;

  insert into public.potd_attempts as a (
    user_id, question_id, solved, solved_at, tests_passed, tests_total
  ) values (
    v_user_id,
    p_question_id,
    coalesce(p_all_passed, false),
    case when coalesce(p_all_passed, false) then now() end,
    p_tests_passed,
    p_tests_total
  )
  on conflict (user_id, question_id) do update
    set solved = a.solved or excluded.solved,
        solved_at = coalesce(a.solved_at, excluded.solved_at),
        tests_passed = case when a.solved then a.tests_passed else excluded.tests_passed end,
        tests_total = case when a.solved then a.tests_total else excluded.tests_total end;
end;
$$;

revoke execute on function public.record_potd_attempt(text, integer, integer, boolean)
  from public, anon;
grant execute on function public.record_potd_attempt(text, integer, integer, boolean)
  to authenticated;

-- Owners may update their row through the RPC only; the RPC is security
-- definer, so no client-facing UPDATE policy is needed or added here.
