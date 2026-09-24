-- Cross-device sync for the two pieces of per-question state that used to
-- live only in one browser's localStorage: the student's in-progress code
-- and the "attempted" set. Solved questions already sync via
-- solved_questions. Both tables are strictly own-row: a signed-in user can
-- only read and write rows where user_id is their own id.

create table public.code_drafts (
  user_id uuid not null references auth.users (id) on delete cascade,
  content_id text not null check (char_length(content_id) between 1 and 120),
  code text not null check (char_length(code) <= 50000),
  updated_at timestamptz not null default now(),
  primary key (user_id, content_id)
);

alter table public.code_drafts enable row level security;

create policy "Users can view their own code drafts"
  on public.code_drafts for select
  using (auth.uid() = user_id);

create policy "Users can insert their own code drafts"
  on public.code_drafts for insert
  with check (auth.uid() = user_id);

create policy "Users can update their own code drafts"
  on public.code_drafts for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create policy "Users can delete their own code drafts"
  on public.code_drafts for delete
  using (auth.uid() = user_id);

create table public.attempted_questions (
  user_id uuid not null references auth.users (id) on delete cascade,
  question_id text not null check (char_length(question_id) between 1 and 120),
  attempted_at timestamptz not null default now(),
  primary key (user_id, question_id)
);

alter table public.attempted_questions enable row level security;

create policy "Users can view their own attempted questions"
  on public.attempted_questions for select
  using (auth.uid() = user_id);

create policy "Users can insert their own attempted questions"
  on public.attempted_questions for insert
  with check (auth.uid() = user_id);

create policy "Users can delete their own attempted questions"
  on public.attempted_questions for delete
  using (auth.uid() = user_id);
