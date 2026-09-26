# 03. Timeouts, Retries, Limits and Fallbacks

The single source for every resilience rule in the project.

## Timeouts

| Where                                                                | Value                    | Behavior on expiry                                                                                                                        |
|-|-|-|
| `functions/_lib/auth.ts` `verifiedUserId` (Supabase `/auth/v1/user`) | 8000 ms                  | Returns `null`, handler answers 401. Thrown errors go to `guard`.                                                                         |
| `functions/_lib/github.ts` `call()` (all GitHub API and OAuth calls) | 8000 ms                  | Throws; `guard` returns `{error:'unavailable'}` 502, `sync` returns `github_failed` 502, `callback` redirects to `/account?github=error`. |
| `functions/accounts/[username].ts` Supabase RPC `get_public_profile` | 5000 ms                  | Falls back to the plain shell with status 200.                                                                                            |
| `github-sync.svelte.ts` `REQUEST_TIMEOUT_MS`                         | 15,000 ms                | Status becomes `unavailable`, sync marked failed.                                                                                         |
| `supabase-drafts-store.ts` all requests                              | 15,000 ms                | Function returns null or does nothing.                                                                                                    |
| `profile-store.ts` load and save                                     | 15,000 ms                | Load returns null; save returns `{ok:false, message}`.                                                                                    |
| `delete-account.ts` RPC                                              | 15,000 ms                | Returns `{ok:false}` with message.                                                                                                        |
| Rating and public profile fetches                                    | 15,000 ms where present  | Return null or empty.                                                                                                                     |
| `supabase-solved-store.ts` all requests                              | 15,000 ms                | Errors are logged; fetch returns empty, writes do nothing.                                                                                |
| Pyodide `runCode`                                                    | 20,000 ms                | Rejects, resets `isRunning`, worker state recovered.                                                                                      |
| Pyodide `runTests`                                                   | 25,000 ms                | Same.                                                                                                                                     |
| `vitest.pyodide.config.ts`                                           | test 60 s, hook 180 s    | Slow suite; downloads the numpy wheel.                                                                                                    |
| OAuth state TTL (`signState`)                                        | 10 min                   | `verifyState` returns null; callback redirects with error.                                                                                |
| Refresh margin (`connection.ts`)                                     | 60 s before expiry       | Token is refreshed early.                                                                                                                 |
| CI jobs                                                              | 3 to 30 min per workflow | See [09](09-ci-testing-ops.md).                                                                                                           |

## Retries

| Where                            | Policy                                                                                                                                                                                                                                       |
|-|-|
| `putFile` (GitHub Contents API)  | 2 attempts. First attempt failing with 409 or 422 (stale sha) re-GETs and retries once. No retry for 401 (returns `unauthorized`) or rate limiting (returns `rate_limited` on 429, or 403 with `x-ratelimit-remaining: 0` or `retry-after`). |
| Token refresh (`usableToken`)    | Refresh tokens are single use. If refresh fails, re-read KV once in case a parallel request already rotated them; if still unusable, delete the connection and return null (client sees `not_connected`, 409).                               |
| `confirmFreshConnection`         | 4 status polls, 1500 ms apart, to ride out KV eventual consistency after the OAuth redirect.                                                                                                                                                 |
| GitHub OAuth callback loop guard | If not installed and `installation_id` is already in the query, stop with an error instead of redirecting to install again.                                                                                                                  |
| Submit to GitHub                 | No automatic retry. On failure the next passing Submit retries.                                                                                                                                                                              |
| Draft sync                       | Failed pushes are retried implicitly: the next edit or the next `syncDrafts` (focus, sign-in) compares timestamps again.                                                                                                                     |
| Progress sync                    | Re-run on tab focus and at sign-in.                                                                                                                                                                                                          |

## Debounce, coalescing and concurrency control

| Mechanism                | Detail                                                                                            |
|-|-|
| Draft push debounce      | `PUSH_DELAY_MS = 1500`                                                                            |
| Draft sync single flight | One shared `running` promise; concurrent callers await the same run                               |
| GitHub sync per question | In flight set plus a queued latest payload; double Submit collapses to at most one extra request  |
| GitHub file writes       | Sequential, not parallel, because parallel commits race on the branch head                        |
| Sync at sign-in          | Keyed on user id so auth event churn does not re-sync                                             |
| `RatingSettle`           | Once per distinct user id                                                                         |
| Pyodide init             | Idempotent; no-op after the worker exists                                                         |
| Rating RPC               | Row lock on `profiles`, unique key on `rating_event` (user, question)                             |
| Question list page reset | Filter edits jump to page 1 after the first mount; first run skipped so `?page=N` survives reload |

## Size and rate limits

| Limit                           | Value                                                            | Enforced in                                              |
|-|-|-|
| `/api/github/sync` request body | 120,000 bytes (413)                                              | `sync.ts`                                                |
| Solution code                   | 50,000 chars                                                     | `solution-files.ts`, DB check                            |
| Description                     | 30,000 chars                                                     | `solution-files.ts`                                      |
| Question id                     | `^[A-Za-z0-9][A-Za-z0-9._-]{0,119}$`, no `..`                    | `isSafeQuestionId` (blocks path traversal into the repo) |
| Title, difficulty, tags         | 200 chars, 40 chars, 20 tags x 40 chars                          | `parseSolutionInput`                                     |
| Commit message                  | 120 chars                                                        | `commitMessage`                                          |
| Draft length                    | 50,000 chars                                                     | `MAX_DRAFT_LENGTH`, DB check                             |
| Draft batch                     | 10 rows and 300,000 chars per request                            | `chunkDrafts`                                            |
| Draft metadata fetch            | 25 ids per request                                               | `IDS_PER_FETCH`                                          |
| Rows per user                   | 1000 for `code_drafts` and `attempted_questions` (errcode 54000) | DB triggers; existing rows still upsert                  |
| Username                        | `^[a-z0-9_]{3,20}$`, unique                                      | `validate-profile.ts` and DB                             |
| Rating floor                    | 400                                                              | SQL and `rating-math.ts`                                 |

## Fallback and degradation rules

| Situation                         | Behavior                                                                           |
|-|-|
| Supabase unreachable              | Local stores keep working. Nothing throws into the UI.                             |
| Functions absent (dev server)     | GitHub sync status becomes `unavailable`.                                          |
| Profile function fails            | Plain shell served with 200; client renders the profile.                           |
| localStorage blocked              | Try/catch around reads and writes; theme, layout and progress just do not persist. |
| Clipboard blocked                 | Copy buttons skip the "copied" state.                                              |
| GitHub star count fetch fails     | Navbar shows no number rather than a fake one.                                     |
| Service worker network failure    | Cached navigation copy served.                                                     |
| Question without authored content | "No IDE content published yet" page, `noindex`.                                    |
| No token, bad JWT                 | 401 `unauthorized`.                                                                |
| Any thrown handler error          | `guard` returns `{error:'unavailable'}` with 502 and `cache-control: no-store`.    |

## Idempotency

`record_potd_outcome` (unique per user and question), `putFile` (skips identical content), solved upsert (unique user and question), draft upsert (unique user and content id), state signature (stateless, verifiable any number of times before expiry).
