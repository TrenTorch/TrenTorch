-- Postgres grants EXECUTE on new functions to the PUBLIC pseudo-role by
-- default; anon/authenticated inherit through that regardless of the
-- earlier per-role revoke, which is why the advisor still flagged this.
revoke execute on function public.handle_new_user() from public;
