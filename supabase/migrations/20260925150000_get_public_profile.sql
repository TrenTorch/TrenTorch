-- The only way an anonymous visitor reads a profile. Returns a fixed set of
-- fields (never alt_email or the user id) and only when the owner ticked
-- "Make my profile public". RLS on profiles stays own-row only.
create or replace function public.get_public_profile(p_username text)
returns table (
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
  select p.username, p.display_name, p.avatar_url, p.organization, p.job_title,
         p.bio, p.location, p.x_url, p.linkedin_url, p.scholar_url, p.github_url,
         p.website_url, p.user_rating,
         (select count(*) from public.solved_questions s where s.user_id = p.id)
  from public.profiles p
  where p.is_public and p.username = lower(p_username)
  limit 1;
$$;

revoke all on function public.get_public_profile(text) from public;
grant execute on function public.get_public_profile(text) to anon, authenticated;
