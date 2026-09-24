-- Extra self-service profile fields. Every column is nullable and owned by
-- the row's own user: the existing "Users can view their own profile" and
-- "Users can update their own profile" policies (auth.uid() = id) already
-- gate reads and writes, and user_rating stays locked by the earlier
-- record_potd_outcome migration. display_name is reused as the person's
-- name, so it is not duplicated here.
alter table public.profiles
  add column if not exists username text,
  add column if not exists organization text,
  add column if not exists job_title text,
  add column if not exists alt_email text,
  add column if not exists bio text,
  add column if not exists location text,
  add column if not exists x_url text,
  add column if not exists linkedin_url text,
  add column if not exists scholar_url text,
  add column if not exists github_url text,
  add column if not exists website_url text,
  add column if not exists is_public boolean not null default false;

-- Usernames are stored lowercase, so a plain unique index is already
-- case-insensitive; the check keeps the stored form canonical.
alter table public.profiles
  add constraint profiles_username_format
    check (username is null or username ~ '^[a-z0-9_]{3,20}$'),
  add constraint profiles_text_lengths check (
    coalesce(char_length(display_name), 0) <= 80
    and coalesce(char_length(organization), 0) <= 100
    and coalesce(char_length(job_title), 0) <= 80
    and coalesce(char_length(alt_email), 0) <= 254
    and coalesce(char_length(bio), 0) <= 280
    and coalesce(char_length(location), 0) <= 80
  ),
  add constraint profiles_link_format check (
    (x_url is null or (x_url ~ '^https://' and char_length(x_url) <= 200))
    and (linkedin_url is null or (linkedin_url ~ '^https://' and char_length(linkedin_url) <= 200))
    and (scholar_url is null or (scholar_url ~ '^https://' and char_length(scholar_url) <= 200))
    and (github_url is null or (github_url ~ '^https://' and char_length(github_url) <= 200))
    and (website_url is null or (website_url ~ '^https?://' and char_length(website_url) <= 200))
  );

create unique index if not exists profiles_username_key on public.profiles (username);
