-- Own-row RLS stops users reading each other's data, but nothing bounded how
-- much one signed-in user could store. content_id is free text (up to 50 KB of
-- code per row), so cap the rows per user. The curriculum has a few hundred
-- questions, so 1000 leaves plenty of headroom for real use.
--
-- A BEFORE INSERT trigger also fires for an upsert that ends up updating an
-- existing row, so a row that already exists is let through: a user at the cap
-- can still edit what they have, just not add new rows.

create or replace function public.cap_code_drafts_per_user()
returns trigger
language plpgsql
as $$
begin
  if exists (
    select 1 from public.code_drafts
    where user_id = new.user_id and content_id = new.content_id
  ) then
    return new;
  end if;
  if (select count(*) from public.code_drafts where user_id = new.user_id) >= 1000 then
    raise exception 'code draft limit reached' using errcode = '54000';
  end if;
  return new;
end;
$$;

create or replace function public.cap_attempted_questions_per_user()
returns trigger
language plpgsql
as $$
begin
  if exists (
    select 1 from public.attempted_questions
    where user_id = new.user_id and question_id = new.question_id
  ) then
    return new;
  end if;
  if (select count(*) from public.attempted_questions where user_id = new.user_id) >= 1000 then
    raise exception 'attempted question limit reached' using errcode = '54000';
  end if;
  return new;
end;
$$;

create trigger code_drafts_row_cap
  before insert on public.code_drafts
  for each row execute function public.cap_code_drafts_per_user();

create trigger attempted_questions_row_cap
  before insert on public.attempted_questions
  for each row execute function public.cap_attempted_questions_per_user();
