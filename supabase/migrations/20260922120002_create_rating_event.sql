-- Audit log for the POTD rating system (potd-rating-system-spec.md §8).
-- Every rating change writes exactly one row here, with the full inputs
-- (rating_before, the anchor and E used, outcome) that produced its delta
-- -- required by §7 so a disputed or suspicious rating change has a real
-- trail, not just a final number.
--
-- No insert/update/delete policy is defined for authenticated/anon on
-- purpose: the only way a row is ever written is the record_potd_outcome()
-- SECURITY DEFINER function (next migration), which computes delta itself
-- instead of accepting one from the client. A client-writable insert policy
-- here would let anyone forge an arbitrary delta straight into their own
-- rating history.
create table public.rating_event (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  question_id text not null,
  potd_date date not null,
  difficulty text not null check (difficulty in ('easy', 'medium', 'hard', 'advanced')),
  anchor_rating integer not null,
  rating_before integer not null,
  expected_e double precision not null,
  outcome text not null check (outcome in ('solved', 'failed')),
  delta integer not null,
  rating_after integer not null,
  created_at timestamptz not null default now(),
  -- One rating event per problem per user, ever (spec §5.1) -- this is also
  -- what makes record_potd_outcome's "already recorded, no-op" check work.
  unique (user_id, question_id)
);

alter table public.rating_event enable row level security;

create policy "Users can view their own rating events"
  on public.rating_event for select
  using (auth.uid() = user_id);

create index rating_event_user_id_idx on public.rating_event (user_id);
