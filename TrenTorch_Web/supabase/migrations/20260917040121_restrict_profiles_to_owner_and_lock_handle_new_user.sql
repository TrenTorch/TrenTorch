-- profiles was readable by anyone (roles: public, qual: true), including
-- fully unauthenticated clients -- that's the "people can see how many
-- users we have" leak: a plain anon-key select('*') on profiles returned
-- every row (id, display_name, avatar_url, created_at, user_rating) for
-- every signed-up user. Nothing in the app actually reads other users'
-- profiles today, so restrict to owner-only, matching the pattern
-- already used on solved_questions and on profiles' own UPDATE policy.
drop policy "Profiles are viewable by everyone" on public.profiles;

create policy "Users can view their own profile"
on public.profiles
for select
to public
using (auth.uid() = id);

-- handle_new_user() is a signup trigger (inserts a profiles row after a
-- new auth.users row is created) -- it was also independently callable
-- by any signed-in or anonymous client directly via
-- /rest/v1/rpc/handle_new_user, running with elevated (SECURITY
-- DEFINER) privileges outside its intended trigger context. Revoke
-- direct execute access; the trigger itself still runs fine since
-- triggers invoke the function independently of role grants.
revoke execute on function public.handle_new_user() from anon, authenticated;
