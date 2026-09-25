-- The record_potd_outcome migration limited what signed-in users may update on
-- profiles to a short column list so that user_rating stays server-only. The
-- self-service profile fields need the same column-level grant. user_rating
-- is deliberately not in this list.
grant update (
  username, organization, job_title, alt_email, bio, location,
  x_url, linkedin_url, scholar_url, github_url, website_url, is_public
) on public.profiles to authenticated;
