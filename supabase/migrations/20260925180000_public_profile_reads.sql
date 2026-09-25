-- A public profile shows the same account page as the owner sees, so the
-- solved list and rating history of someone who ticked "Make my profile
-- public" become readable by anyone. Nobody else's rows are opened, and
-- private profiles stay own-row only.
create or replace function public.is_public_user(uid uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (select 1 from public.profiles p where p.id = uid and p.is_public);
$$;

revoke all on function public.is_public_user(uuid) from public;
grant execute on function public.is_public_user(uuid) to anon, authenticated;

create policy "Anyone can view a public user's solved questions"
  on public.solved_questions for select
  to anon, authenticated
  using (public.is_public_user(user_id));

create policy "Anyone can view a public user's rating events"
  on public.rating_event for select
  to anon, authenticated
  using (public.is_public_user(user_id));

-- Column grants for visitors who are not signed in: only what the graphs draw.
grant select (user_id, question_id, solved_at) on public.solved_questions to anon;
grant select (user_id, created_at, question_id, outcome, delta, rating_before, rating_after)
  on public.rating_event to anon;

-- The profile lookup now also returns the id, used only to read the two
-- tables above. alt_email is still never returned.
drop function if exists public.get_public_profile(text);
create function public.get_public_profile(p_username text)
returns table (
  id uuid,
  username text,
  display_name text,
  avatar_url text,
  organization text,
  job_title text,
  bio text,
  location text,
  x_url text,
  linkedin_url text,
  scholar_url text,
  github_url text,
  website_url text,
  user_rating integer,
  solved_count bigint
)
language sql
stable
security definer
set search_path = public
as $$
  select p.id, p.username, p.display_name, p.avatar_url, p.organization, p.job_title,
         p.bio, p.location, p.x_url, p.linkedin_url, p.scholar_url, p.github_url,
         p.website_url, p.user_rating,
         (select count(*) from public.solved_questions s where s.user_id = p.id)
  from public.profiles p
  where p.is_public and p.username = lower(p_username)
  limit 1;
$$;

revoke all on function public.get_public_profile(text) from public;
grant execute on function public.get_public_profile(text) to anon, authenticated;
