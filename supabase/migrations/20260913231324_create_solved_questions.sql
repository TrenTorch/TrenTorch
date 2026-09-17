create table public.solved_questions (
  user_id uuid not null references auth.users (id) on delete cascade,
  question_id text not null,
  is_potd boolean not null default false,
  solved_at timestamptz not null default now(),
  primary key (user_id, question_id)
);

alter table public.solved_questions enable row level security;

create policy "Users can view their own solved questions"
  on public.solved_questions for select
  using (auth.uid() = user_id);

create policy "Users can insert their own solved questions"
  on public.solved_questions for insert
  with check (auth.uid() = user_id);

create policy "Users can update their own solved questions"
  on public.solved_questions for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create policy "Users can delete their own solved questions"
  on public.solved_questions for delete
  using (auth.uid() = user_id);

create index solved_questions_user_id_idx on public.solved_questions (user_id);
