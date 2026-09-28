-- POTD discussion: one comment per solver per question, flat votes only.
-- Postgres is the enforcement layer because the app is statically hosted.

create function public.is_potd_unlocked(q_id text)
returns boolean
language sql
stable
set search_path = ''
as $$
  select exists (
    select 1
    from public.potd_schedule s
    where s.question_id = q_id
      and now() >= (((s.potd_date + 1)::timestamp) at time zone 'UTC') + interval '12 hours'
  );
$$;

create function public.has_solved(u_id uuid, q_id text)
returns boolean
language sql
stable
set search_path = ''
as $$
  select exists (
    select 1
    from public.solved_questions sq
    where sq.user_id = u_id and sq.question_id = q_id
  );
$$;

revoke execute on function public.is_potd_unlocked(text) from public, anon;
revoke execute on function public.has_solved(uuid, text) from public, anon;
grant execute on function public.is_potd_unlocked(text) to authenticated;
grant execute on function public.has_solved(uuid, text) to authenticated;

create table public.potd_discussion_comments (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid not null default auth.uid() references auth.users (id) on delete cascade,
  question_id text not null references public.potd_schedule (question_id) on delete cascade,
  content     text not null check (char_length(content) between 1 and 2000),
  upvotes     int4 not null default 0,
  downvotes   int4 not null default 0,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  constraint one_comment_per_user_per_question unique (user_id, question_id)
);

create index potd_discussion_comments_question_idx
  on public.potd_discussion_comments (question_id);

alter table public.potd_discussion_comments enable row level security;

revoke all on public.potd_discussion_comments from anon, authenticated;
grant select on public.potd_discussion_comments to authenticated;
grant insert (question_id, content) on public.potd_discussion_comments to authenticated;
grant update (content) on public.potd_discussion_comments to authenticated;
grant delete on public.potd_discussion_comments to authenticated;

create policy "Authors can view their own comment"
  on public.potd_discussion_comments for select
  to authenticated
  using (auth.uid() = user_id);

create policy "Anyone signed in can view comments once the POTD is unlocked"
  on public.potd_discussion_comments for select
  to authenticated
  using (public.is_potd_unlocked(question_id));

create policy "Solvers can post their comment"
  on public.potd_discussion_comments for insert
  to authenticated
  with check (auth.uid() = user_id and public.has_solved(auth.uid(), question_id));

create policy "Authors can edit their own comment"
  on public.potd_discussion_comments for update
  to authenticated
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create policy "Authors can delete their own comment"
  on public.potd_discussion_comments for delete
  to authenticated
  using (auth.uid() = user_id);

create function public.validate_potd_comment()
returns trigger
language plpgsql
set search_path = ''
as $$
declare
  body text := replace(new.content, E'\r', '');
  blk  text;
  line text;
  run  int := 0;
  max_block constant int := 6;
  max_lines constant int := 30;
begin
  if (select count(*) from regexp_split_to_table(body, E'\n')) > max_lines then
    raise exception 'potd_comment_too_many_lines' using errcode = 'check_violation';
  end if;

  for blk in
    select m[2] from regexp_matches(body, E'(```|~~~)[^\\n]*\\n(.*?)(?:\\1|$)', 'gs') as m
  loop
    if (select count(*) from regexp_split_to_table(blk, E'\n') l where btrim(l) <> '') > max_block then
      raise exception 'potd_comment_code_block_too_long' using errcode = 'check_violation';
    end if;
  end loop;

  for line in select * from regexp_split_to_table(body, E'\n') loop
    if line ~ E'^(    |\\t)' and btrim(line) <> '' then
      run := run + 1;
      if run > max_block then
        raise exception 'potd_comment_code_block_too_long' using errcode = 'check_violation';
      end if;
    else
      run := 0;
    end if;
  end loop;

  if tg_op = 'UPDATE' then
    new.updated_at := now();
  end if;
  return new;
end;
$$;

revoke execute on function public.validate_potd_comment() from public, anon, authenticated;

create trigger validate_potd_comment
  before insert or update of content on public.potd_discussion_comments
  for each row execute function public.validate_potd_comment();

create table public.potd_comment_votes (
  user_id    uuid not null default auth.uid() references auth.users (id) on delete cascade,
  comment_id uuid not null references public.potd_discussion_comments (id) on delete cascade,
  vote_value int2 not null check (vote_value in (-1, 1)),
  created_at timestamptz not null default now(),
  primary key (user_id, comment_id)
);

alter table public.potd_comment_votes enable row level security;

revoke all on public.potd_comment_votes from anon, authenticated;
grant select on public.potd_comment_votes to authenticated;
grant insert (comment_id, vote_value) on public.potd_comment_votes to authenticated;
grant update (vote_value) on public.potd_comment_votes to authenticated;
grant delete on public.potd_comment_votes to authenticated;

create policy "Users can view their own votes"
  on public.potd_comment_votes for select
  to authenticated
  using (auth.uid() = user_id);

create policy "Users can vote on visible comments that are not their own"
  on public.potd_comment_votes for insert
  to authenticated
  with check (
    auth.uid() = user_id
    and exists (
      select 1
      from public.potd_discussion_comments c
      where c.id = comment_id and c.user_id <> auth.uid()
    )
  );

create policy "Users can change their own vote"
  on public.potd_comment_votes for update
  to authenticated
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create policy "Users can retract their own vote"
  on public.potd_comment_votes for delete
  to authenticated
  using (auth.uid() = user_id);

create function public.apply_potd_vote_delta()
returns trigger
language plpgsql
security definer set search_path = ''
as $$
declare
  du int := 0;
  dd int := 0;
  target uuid;
begin
  if tg_op in ('UPDATE', 'DELETE') then
    if old.vote_value = 1 then du := du - 1; else dd := dd - 1; end if;
    target := old.comment_id;
  end if;
  if tg_op in ('INSERT', 'UPDATE') then
    if new.vote_value = 1 then du := du + 1; else dd := dd + 1; end if;
    target := new.comment_id;
  end if;

  update public.potd_discussion_comments
     set upvotes = upvotes + du, downvotes = downvotes + dd
   where id = target;

  if tg_op = 'DELETE' then return old; end if;
  return new;
end;
$$;

revoke execute on function public.apply_potd_vote_delta() from public, anon, authenticated;

create trigger apply_potd_vote_delta
  after insert or update of vote_value or delete on public.potd_comment_votes
  for each row execute function public.apply_potd_vote_delta();

create function public.get_potd_discussion_state(p_question_id text)
returns table (unlocked boolean, solved boolean, has_commented boolean)
language sql
stable
set search_path = ''
as $$
  select
    public.is_potd_unlocked(p_question_id),
    public.has_solved(auth.uid(), p_question_id),
    exists (
      select 1 from public.potd_discussion_comments c
      where c.question_id = p_question_id and c.user_id = auth.uid()
    );
$$;

create function public.get_potd_comments(p_question_id text)
returns table (
  id uuid,
  content text,
  upvotes int4,
  downvotes int4,
  created_at timestamptz,
  updated_at timestamptz,
  is_mine boolean,
  my_vote int2,
  author_username text,
  author_display_name text
)
language sql
stable
security definer set search_path = ''
as $$
  select
    c.id, c.content, c.upvotes, c.downvotes, c.created_at, c.updated_at,
    (c.user_id = auth.uid()),
    v.vote_value,
    case when p.is_public then p.username end,
    case when p.is_public then p.display_name end
  from public.potd_discussion_comments c
  left join public.profiles p on p.id = c.user_id
  left join public.potd_comment_votes v
    on v.comment_id = c.id and v.user_id = auth.uid()
  where auth.uid() is not null
    and c.question_id = p_question_id
    and (c.user_id = auth.uid() or public.is_potd_unlocked(p_question_id))
  order by (c.upvotes - c.downvotes) desc, c.created_at asc
  limit 200;
$$;

revoke execute on function public.get_potd_discussion_state(text) from public, anon;
revoke execute on function public.get_potd_comments(text) from public, anon;
grant execute on function public.get_potd_discussion_state(text) to authenticated;
grant execute on function public.get_potd_comments(text) to authenticated;
