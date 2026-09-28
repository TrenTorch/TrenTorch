-- Rating writes are server-authoritative: only the scheduled day's POTD may
-- award a solve, failures settle only genuine unsolved attempts, and retries
-- cannot race into duplicate rating events.
create function public.guard_potd_rating_event()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
declare
  scheduled_date date;
  scheduled_difficulty text;
  expected_e double precision;
  expected_delta integer;
  scheduled_anchor integer;
  today_utc date := (now() at time zone 'UTC')::date;
begin
  perform pg_advisory_xact_lock(hashtextextended(new.user_id::text, 0));

  if exists (
    select 1
    from public.rating_event existing
    where existing.user_id = new.user_id
      and existing.question_id = new.question_id
  ) then
    raise exception 'potd_rating_already_recorded'
      using errcode = 'unique_violation';
  end if;

  select s.potd_date, s.difficulty
    into scheduled_date, scheduled_difficulty
    from public.potd_schedule s
    where s.question_id = new.question_id;

  if scheduled_date is null
    or new.potd_date <> scheduled_date
    or new.difficulty <> scheduled_difficulty
  then
    raise exception 'potd_rating_schedule_mismatch'
      using errcode = 'check_violation';
  end if;

  if new.outcome = 'solved' then
    if today_utc <> scheduled_date then
      raise exception 'potd_solve_rating_only_available_on_scheduled_day'
        using errcode = 'check_violation';
    end if;

    if not exists (
      select 1
      from public.potd_attempts a
      where a.user_id = new.user_id
        and a.question_id = new.question_id
        and a.solved
        and (a.first_attempted_at at time zone 'UTC')::date = scheduled_date
        and (a.solved_at at time zone 'UTC')::date = scheduled_date
    ) then
      raise exception 'potd_solve_attempt_not_recorded'
        using errcode = 'check_violation';
    end if;
  elsif new.outcome = 'failed' then
    if today_utc <= scheduled_date then
      raise exception 'potd_failure_rating_must_settle_after_scheduled_day'
        using errcode = 'check_violation';
    end if;

    if not exists (
      select 1
      from public.potd_attempts a
      where a.user_id = new.user_id
        and a.question_id = new.question_id
        and not a.solved
        and (a.first_attempted_at at time zone 'UTC')::date = scheduled_date
    ) then
      raise exception 'potd_failure_requires_unsolved_attempt_on_scheduled_day'
        using errcode = 'check_violation';
    end if;
  else
    raise exception 'potd_rating_outcome_invalid'
      using errcode = 'check_violation';
  end if;

  scheduled_anchor := case new.difficulty
    when 'easy' then 550
    when 'medium' then 850
    when 'hard' then 1250
    when 'advanced' then 1850
    else null
  end;

  if scheduled_anchor is null or new.anchor_rating <> scheduled_anchor then
    raise exception 'potd_rating_anchor_invalid'
      using errcode = 'check_violation';
  end if;

  expected_e := 1.0 / (
    1.0 + power(10.0, (new.anchor_rating - new.rating_before)::double precision / 400.0)
  );

  if new.outcome = 'solved' then
    expected_delta := round(100.0 * (1.0 - expected_e))::integer;
  else
    expected_delta := greatest(
      400 - new.rating_before,
      -round(20.0 * expected_e)::integer
    );
  end if;

  if abs(new.expected_e - expected_e) > 0.000000001
    or new.delta <> expected_delta
    or new.rating_after <> new.rating_before + expected_delta
    or new.rating_after < 400
  then
    raise exception 'potd_rating_calculation_mismatch'
      using errcode = 'check_violation';
  end if;

  return new;
end;
$$;

revoke execute on function public.guard_potd_rating_event() from public, anon, authenticated;

do $$
begin
  if to_regclass('public.rating_event') is null
    or to_regclass('public.potd_attempts') is null
    or to_regclass('public.potd_schedule') is null
  then
    raise exception 'POTD rating tables are required before installing rating event guards';
  end if;

  if not exists (
    select 1
    from pg_trigger t
    where t.tgname = 'guard_potd_rating_event'
      and t.tgrelid = to_regclass('public.rating_event')
      and not t.tgisinternal
  ) then
    execute 'create trigger guard_potd_rating_event
      before insert on public.rating_event
      for each row execute function public.guard_potd_rating_event()';
  end if;
end;
$$;
