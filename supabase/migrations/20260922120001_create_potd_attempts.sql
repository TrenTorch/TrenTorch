-- Server-side twin of processes/progress-tracking/attempted.svelte.ts's
-- localStorage set, scoped to POTD only. Rating's "failed" outcome (spec
-- 5.4: not-attempted is neutral, attempted-and-not-solved costs points)
-- needs a durable, cross-device signal of "did this user ever submit
-- against this POTD problem" -- localStorage alone can't answer that when
-- the day-end settlement check (processes/rating/settle-past-potd.ts) runs
-- from a different browser/device than the one the attempt happened on.
create table public.potd_attempts (
  user_id uuid not null references auth.users (id) on delete cascade,
  question_id text not null,
  first_attempted_at timestamptz not null default now(),
  primary key (user_id, question_id)
);

alter table public.potd_attempts enable row level security;

create policy "Users can view their own POTD attempts"
  on public.potd_attempts for select
  using (auth.uid() = user_id);

create policy "Users can record their own POTD attempts"
  on public.potd_attempts for insert
  with check (auth.uid() = user_id);

create index potd_attempts_user_id_idx on public.potd_attempts (user_id);
