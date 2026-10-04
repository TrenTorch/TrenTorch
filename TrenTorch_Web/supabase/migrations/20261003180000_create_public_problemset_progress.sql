create or replace function public.get_public_problemset_solved(p_username text)
returns table (question_id text)
language sql
stable
security definer
set search_path = ''
as $$
	select solved.question_id
	from public.solved_questions as solved
	join public.profiles as profile on profile.id = solved.user_id
	where lower(profile.username) = lower(trim(p_username))
		and profile.is_public is true
		and solved.question_id like 'problem-%';
$$;

revoke all on function public.get_public_problemset_solved(text) from public;
grant execute on function public.get_public_problemset_solved(text) to anon, authenticated;
