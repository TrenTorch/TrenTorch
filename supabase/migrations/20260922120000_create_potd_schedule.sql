-- Server-side mirror of data/potd.ts. The rating RPC (see the
-- record_potd_outcome migration) must never trust a client-supplied
-- difficulty or problem_id for a rating change -- a client that could pick
-- its own difficulty could claim 'advanced' on an easy problem for a huge
-- fake gain, and a client that could pick its own problem_id could farm
-- unlimited rating with made-up ids (the per-(user,problem) uniqueness on
-- rating_event only stops replaying the SAME id, not inventing new ones).
-- This table is what the RPC looks the real difficulty up in instead.
--
-- Keep this in sync with data/potd.ts by hand: adding a new POTD entry
-- there also means inserting its row here in a follow-up migration.
create table public.potd_schedule (
  question_id text primary key,
  potd_date date not null,
  difficulty text not null check (difficulty in ('easy', 'medium', 'hard', 'advanced'))
);

alter table public.potd_schedule enable row level security;

-- Read-only reference data every signed-in student needs (the client picks
-- the right anchor/difficulty to *display*, e.g. a "you'd gain ~X" preview,
-- even though the RPC re-derives it server-side rather than trusting that
-- display value back).
create policy "Anyone signed in can read the POTD schedule"
  on public.potd_schedule for select
  to authenticated
  using (true);

-- data/potd.ts's one entry today, difficulty from
-- data/curriculum/generated-curriculum.json (GeneratedQuestion.difficulty
-- 'Advanced' maps to the rating system's 'hard' -- see
-- processes/rating/rating-math.ts's RATING_DIFFICULTY_MAP for why the
-- mapping isn't 1:1 on the name).
insert into public.potd_schedule (question_id, potd_date, difficulty) values
  ('regularized-linear-models-ridge-regression-gaussian-elimination', '2026-09-14', 'hard');
