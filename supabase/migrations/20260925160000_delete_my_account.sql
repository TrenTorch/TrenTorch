-- Lets a signed-in user delete their own account. Every table in public
-- (profiles, solved_questions, potd_attempts, rating_event, code_drafts,
-- attempted_questions) references auth.users on delete cascade, so removing
-- the auth row removes all of their data. Only the caller's own row is ever
-- touched: the id comes from auth.uid(), never from an argument.
create or replace function public.delete_my_account()
returns void
language plpgsql
security definer
set search_path = public, auth
as $$
begin
  if auth.uid() is null then
    raise exception 'not signed in';
  end if;
  delete from auth.users where id = auth.uid();
end;
$$;

revoke all on function public.delete_my_account() from public, anon;
grant execute on function public.delete_my_account() to authenticated;
