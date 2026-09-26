# 06. Database (Supabase)

Project `axgzkiqhelozgouszgex`. The browser talks to it with the anon key and the user's JWT. Access control is RLS, column grants, and SECURITY DEFINER functions. Migrations live in `supabase/migrations/` (dated 2026-09-22 to 2026-09-25).

Important: `profiles` and `solved_questions` were created earlier outside this repo, so the migrations only alter or add to them. A fresh database cannot be rebuilt from the migrations alone.

## Tables

| Table                 | Purpose                                                                     | Access model                                                                                                                                     |
|-|-|-|
| `profiles`            | One row per user: display name, username, links, `is_public`, `user_rating` | Users update only self service columns (grant update on those). `user_rating` update is revoked; only the RPC changes it. Unique username index. |
| `solved_questions`    | (user, question, solved_at)                                                 | Own rows read and write. Anon and authenticated can select rows of users whose profile is public (`is_public_user`), with column grants to anon. |
| `attempted_questions` | (user, question)                                                            | Own rows only. Per user cap 1000.                                                                                                                |
| `code_drafts`         | (user, content id, code, updated_at)                                        | Own rows only. Code length check 50,000. Per user cap 1000.                                                                                      |
| `potd_schedule`       | Server mirror of `data/potd.ts` (date, question id, difficulty)             | Read for validation inside RPCs. Seeded with one row only (see [10](10-known-drift.md)).                                                         |
| `potd_attempts`       | Per attempt history for POTD questions (counts, score)                      | Own rows.                                                                                                                                        |
| `rating_event`        | Audit log of every rating change (before, after, outcome)                   | Unique per user and question. No client write policy. Public read for public profiles.                                                           |

Caps use triggers raising errcode 54000; rows that already exist still pass so upserts to existing ids never fail after the cap is reached.

## Profile field rules

Username `^[a-z0-9_]{3,20}$` (mirrors `validate-profile.ts`), length limits on text fields, links must be https, and unique username index. `is_public` gates every public read.

## Functions

| Function                                        | Security         | Behavior                                                                                                                                                                                                                              |
|-|-|-|
| `record_potd_outcome(p_question_id, p_outcome)` | SECURITY DEFINER | Validates the question is scheduled and its date rules, locks the user's profile row, computes the rating change, inserts `rating_event`, updates `profiles.user_rating`, returns before and after. Idempotent per user and question. |
| `get_public_profile(username)`                  | SECURITY DEFINER | Returns the public fields (and the user `id`) for a public profile, nothing for private or missing.                                                                                                                                   |
| `delete_my_account()`                           | SECURITY DEFINER | Deletes the caller's `auth.users` row; foreign keys cascade to all user tables.                                                                                                                                                       |
| `is_public_user(uid)`                           | helper           | Used by select policies on `solved_questions` and `rating_event`.                                                                                                                                                                     |
| cap triggers                                    | trigger          | Enforce the 1000 row limit.                                                                                                                                                                                                           |

## Rating math (SQL and TypeScript mirror)

Anchors by difficulty: easy 550, medium 850, hard 1250, advanced 1850. Expected solve probability `E = 1 / (1 + 10^((anchor - rating) / 400))`. Solved gain `round(100 x (1 - E))` (K_GAIN 100). Failed loss `round(20 x E)` (K_LOSS 20). Rating never falls below 400. New users start at 400.

Tiers: Hello World 400 to 700, Segfault Survivor 700 to 1000, Knight of the Kernel 1000 to 1500, Ace of Attention 1500 to 1700, Conqueror of CUDA 1700 to 2000, Singularity 2000 and above. Interview referral eligibility needs 7 consecutive `rating_after` values at or above 1500 (`qualifiesForInterviewReferral`).

`processes/rating/rating-math.ts` must stay identical to the SQL; the SQL is authoritative, the TypeScript is used for the UI (tiers, chart bands, previews).

## Client to database map

| Client function                                                                               | Table or RPC                                        |
|-|-|
| `fetchSolvedQuestions`, `upsertSolvedQuestion(s)`, `deleteSolvedQuestion`, `fetchSolvedDates` | `solved_questions`                                  |
| `fetchAttempted`, `upsertAttempted`, `deleteAttempted`                                        | `attempted_questions`                               |
| `fetchDraftMeta`, `fetchDraftCodes`, `upsertDrafts`, `deleteDraft`                            | `code_drafts`                                       |
| `recordPotdAttempt` (rating store)                                                            | `potd_attempts` upsert                              |
| `recordPotdAttempt` (potd attempts store)                                                     | RPC `record_potd_attempt` (no migration defines it) |
| `recordPotdOutcome`                                                                           | RPC `record_potd_outcome`                           |
| `fetchUnratedPastAttempts`, `fetchRatingHistory`                                              | `potd_attempts`, `rating_event`                     |
| `loadProfile`, `saveProfile`                                                                  | `profiles`                                          |
| `fetchPublicProfile`, Function profile page                                                   | RPC `get_public_profile`                            |
| `deleteAccount`                                                                               | RPC `delete_my_account`                             |
