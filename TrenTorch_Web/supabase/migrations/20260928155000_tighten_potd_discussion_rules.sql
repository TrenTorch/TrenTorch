-- Require a recorded POTD solve (not merely solving the same curriculum
-- question) and reveal past discussions as soon as their UTC day has passed.
create or replace function public.is_potd_unlocked(q_id text)
returns boolean
language sql
stable
set search_path = ''
as $$
  select exists (
    select 1
    from public.potd_schedule s
    where s.question_id = q_id
      and (now() at time zone 'UTC')::date > s.potd_date
  );
$$;

create or replace function public.has_solved(u_id uuid, q_id text)
returns boolean
language sql
stable
set search_path = ''
as $$
  select exists (
    select 1
    from public.solved_questions sq
    where sq.user_id = u_id
      and sq.question_id = q_id
      and sq.is_potd
  );
$$;

create or replace function public.validate_potd_comment()
returns trigger
language plpgsql
set search_path = ''
as $$
declare
  body text := replace(new.content, E'\r', '');
  body_without_fenced_blocks text;
  blk text;
  line text;
  run int := 0;
  code_lines int := 0;
  max_block constant int := 6;
  max_lines constant int := 30;
begin
  if (select count(*) from regexp_split_to_table(body, E'\n')) > max_lines then
    raise exception 'potd_comment_too_many_lines' using errcode = 'check_violation';
  end if;

  for blk in
    select m[2] from regexp_matches(body, E'(```|~~~)[^\\n]*\\n(.*?)(?:\\1|$)', 'gs') as m
  loop
    code_lines := code_lines + (
      select count(*) from regexp_split_to_table(blk, E'\n') l where btrim(l) <> ''
    );
    if code_lines > max_block then
      raise exception 'potd_comment_code_block_too_long' using errcode = 'check_violation';
    end if;
  end loop;

  body_without_fenced_blocks :=
    regexp_replace(body, E'(```|~~~)[^\\n]*\\n.*?(?:\\1|$)', '', 'gs');
  for line in select * from regexp_split_to_table(body_without_fenced_blocks, E'\n') loop
    if line ~ E'^(    |\\t)' and btrim(line) <> '' then
      run := run + 1;
      code_lines := code_lines + 1;
      if code_lines > max_block then
        raise exception 'potd_comment_code_block_too_long' using errcode = 'check_violation';
      end if;
    else
      run := 0;
    end if;
  end loop;

  if tg_op = 'UPDATE' then
    new.updated_at := now();
  end if;
  return new;
end;
$$;

revoke execute on function public.is_potd_unlocked(text) from public, anon;
grant execute on function public.is_potd_unlocked(text) to authenticated;
revoke execute on function public.has_solved(uuid, text) from public, anon;
grant execute on function public.has_solved(uuid, text) to authenticated;
revoke execute on function public.validate_potd_comment() from public, anon, authenticated;
