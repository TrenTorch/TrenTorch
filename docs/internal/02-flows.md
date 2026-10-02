# 02. Flows

Each flow lists the trigger, the steps in order, and what happens on failure.

## 1. Sign-in and session

Files: `processes/auth/session.svelte.ts`, `supabase-client.ts`, `gate-behind-sign-in.ts`, `after-sign-in-destination.ts`, `sign-in-prompt.svelte.ts`, `preview-mode.ts`; components `SignInDialog`, `AuthPanel`, `AfterSignInRedirect`, `AccountButton`.

1. `getSupabaseClient()` lazily creates one browser only client (throws on the server).
2. `session.svelte.ts` holds module level `$state` (`user`, `accessToken`, loading flag). It calls `getSession()` once and subscribes to `onAuthStateChange`, so every method below ends by updating the same state.
3. Sign-in methods: `signInWithGitHub`, `signInWithGoogle` (OAuth redirect), `signInWithMagicLink(email)`. All use `redirectTo = ${origin}/account`.
4. Gating: a plain click on Navbar links marked `gated` (Questions, POTD) calls `gateBehindSignIn`. If signed out it prevents navigation, stores the destination in sessionStorage (`trentorch-after-sign-in`, same-site paths only) and opens the dialog with reason `browse`. Pages stay public and crawlable because the hrefs are real links.
5. Run and Submit on the IDE page open the dialog with reason `run` when signed out, unless `signInSkipped()` (preview builds).
6. When a session appears, `SignInDialog` closes itself and `AfterSignInRedirect` navigates to the remembered destination. Dismissing the dialog forgets the destination.

Failure: Supabase errors surface in the auth panel. The client never throws into the UI on session lookup.

## 2. Progress sync (solved and attempted)

Files: `solved.svelte.ts`, `attempted.svelte.ts`, `sync-solved-with-supabase.ts`, `sync-attempted-with-supabase.ts`, `supabase-solved-store.ts`, `supabase-drafts-store.ts`, component `ProgressSync`.

1. Signed out: both stores read and write localStorage (`trentorch-solved-questions`, `trentorch-attempted-questions`) only.
2. Signed in: `ProgressSync` runs once per distinct user id (keyed on id, because `session.user` is a new object on every auth event) and again whenever the tab becomes visible. Each sync is wrapped so one failing store never blocks the others.
3. Solved sync is a two way union: fetch remote rows, merge remote slugs into local through `markSolvedFromRemote`, upload local slugs that remote lacks with `upsertSolvedQuestions`.
4. Attempted sync does the same against `attempted_questions`.
5. Afterwards, individual `markSolved` and `markAttempted` calls also push a single row fire and forget. `unmarkSolved` and `unmarkAttempted` delete the remote row.
6. Solved is earned only by a passing Submit (`markSolved`). `markSolvedFromRemote` exists so a remote row is never echoed back.

Failure: every remote function catches and logs, returning `null`, `[]` or nothing. Local state is never rolled back.

## 3. Draft sync (editor contents across devices)

Files: `save-user-code.ts`, `load-user-code.ts`, `reset-user-code.ts`, `draft-sync.svelte.ts`, `supabase-drafts-store.ts`.

1. Every keystroke calls `saveUserCode(id, code)`: writes `trentorch_code_<id>`, writes a timestamp stamp `trentorch_codemeta_<id>` (`stampLocalDraft`), and calls `queueDraftPush`.
2. `queueDraftPush` debounces 1500 ms per burst and then uploads through `upsertDrafts`, batched (at most 10 rows and 300,000 characters per request).
3. On sign-in or focus, `syncDrafts(userId)` shares one in flight promise. It first downloads only metadata (`fetchDraftMeta`: id plus timestamp), compares timestamps with local stamps, and downloads code (`fetchDraftCodes`, 25 ids per request) only for rows newer remotely. Newest edit wins. Local drafts newer than remote are uploaded.
4. `draftSync.version` increments when remote code was pulled; the IDE page watches it and reloads the editor if the student has not typed since load (`editedSinceLoad`), so a sync never overwrites live typing.
5. Reset removes local code plus stamp and deletes the remote draft.

Failure: no function throws. A 15 second timeout guards each request. Drafts longer than 50,000 characters are skipped (also enforced by a DB check).

## 4. Running code (Run and Submit)

Files: `pyodide-service.ts`, `pyodide-worker.ts`, `initialize-pyodide.ts`, `pyodide-setup-script.ts`, `build-test-runner-script.ts`, `ide-content/*`.

1. Page load: the IDE page calls `pyodideService.init()` (idempotent) when content exists. It creates the worker. The worker dynamically imports Pyodide 0.27.2 from jsDelivr through `new Function('u', 'return import(u)')` (so Vite does not try to bundle it), loads it, then preloads `numpy`. States: `uninitialized`, `loading_runtime`, `loading_packages`, `ready`, `running`, `testing`, `error`.
2. Run: `runTests(code, harness, id, limit = 2)`. Submit: `runTests(code, harness, id)` (no limit).
3. The service allocates a request id, stores a resolver in a pending map, and posts the message with a timeout (20 s for `runCode`, 25 s for `runTests`). On timeout it rejects and resets `isRunning`.
4. The worker prepends `SETUP_SCRIPT` (works around an interpreter globals ordering race, wires `OutputCapture`), runs the script built by `buildTestRunnerScript`, and posts results.
5. The harness is generated at build time per question (see [07](07-content-pipeline.md)). The test collector prints a machine readable results block that the service parses into `SingleTestResult[]` and `SubmissionResult`.
6. Submit only: `attempted.markAttempted(result.contentId)` then, if all passed, `solved.markSolved` and GitHub sync. The id used is `result.contentId`, not the currently displayed question, so navigating away mid run never marks the wrong question.

Failure: a rejected promise writes `[Run failed]: message` or `[Submit failed]: message` into the console tab. The worker checks message origin. Worker `onerror` sets state `error`.

## 5. GitHub sync of accepted solutions

Files: client `github-sync.svelte.ts`, components `GithubSyncCard`; server `functions/api/github/*`, `functions/_lib/*`.

Connect:

1. `connectGithub()` POSTs `/api/github/start` with the Supabase access token as Bearer.
2. `start.ts` verifies the JWT (`verifiedUserId`, 8 s call to Supabase `/auth/v1/user`), signs an OAuth state (`signState`, HMAC-SHA256, 10 minute TTL) and returns the GitHub authorize URL.
3. Browser goes to GitHub, then back to `/api/github/callback?code&state`.
4. `callback.ts` verifies the state, exchanges the code (`exchangeCode`), reads the login (`getLogin`), and asks `findRepoAccess` whether the GitHub App is installed with access to `trentorch-solutions`. If not installed it redirects to the install URL once; if `installation_id` is already present it stops with an error instead of looping.
5. Tokens are stored encrypted in KV (`storeTokens`, AES-GCM, random IV). Redirect to `/account?github=connected`, or `/account?github=error` on any throw.
6. On return, `GithubSyncCard` calls `confirmFreshConnection()`: it polls `/api/github/status` up to 4 times, 1500 ms apart, because KV is eventually consistent.

Sync on Submit:

1. After a fully passing Submit, `syncSolutionToGithub(payload)` runs (fire and forget). One request per question at a time; a second Submit while one is in flight replaces the queued payload (coalescing).
2. POST `/api/github/sync`. Server: verify JWT, cap body at 120,000 bytes, `parseSolutionInput`, `usableToken` (refreshes if within 60 s of expiry, see [03](03-resilience.md)), then `putFile` for `solutions/<id>/solution.py` and `solutions/<id>/README.md`, sequentially.
3. `putFile` GETs the existing file for its sha, skips the commit if content is identical, PUTs, and retries once on 409 or 422.
4. Status codes map to client state: 409 `not_connected` marks disconnected; any other failure keeps status and shows "retries on your next passing submit".

Disconnect: `/api/github/disconnect` revokes the grant at GitHub then deletes the KV entry. Account deletion calls this first.

## 6. Problem of the Day and rating

Files: `data/potd.ts`, `processes/potd/*`, `processes/rating/*`, migrations, components `RatingBadge`, `RatingHistory`, `RatingSettle`.

1. Schedule: `potdEntries` (date, questionId, difficulty). Which entry is "today" is decided in the browser from the visitor's local date (`localDateString`), never at build time, so the prerendered page is date independent. Build time only computes small summaries (`toPotdSummary`).
2. `getTodaysPotd`, `getTodaysPotdPart` and `getPastPotdPart` produce today's and past sections. Future entries are hidden. The IDE guide shows only Description for today or future POTDs, Description and Theory once the day has passed, and never Solution.
3. On Submit of a POTD question (signed in): `recordPotdAttemptHistory` (RPC `record_potd_attempt`, see drift note) and `recordPotdAttempt` (upsert into `potd_attempts`) are fired. On a pass, `recordPotdOutcome(id, 'solved')` calls RPC `record_potd_outcome`, which computes the new rating in SQL, and the client updates `ratingStore`.
4. Failures are lazy: there is no cron. `RatingSettle` runs at sign-in and calls `settlePastPotdOutcomes`, which finds past POTDs that were attempted but have no rating event and records `'failed'` outcomes (loss = round(20 x expected solve probability), floored at 400).
5. The RPC is idempotent (unique per user and question on `rating_event`), locks the profile row, and is the only path that changes `profiles.user_rating`.

## 7. Static generation and SEO

1. `/ide/[id]/+page.server.ts` `entries()` returns every curriculum slug plus every authored question id, so all pages exist as files. Unauthored slugs render a "not published yet" state and are `noindex`.
2. `load` runs once per page at build: content, adjacent ids, SEO block (`buildQuestionSeo`), company tags.
3. `SEO.svelte` renders title, description, canonical, Open Graph, Twitter tags and JSON-LD through `toJsonLdScript` (escapes `<`).
4. `sitemap.xml/+server.ts` is prerendered from `listSitemapPaths` (static paths, Parts, authored questions; future POTDs excluded using `latestLiveDate`, which shifts to UTC+14 so the earliest timezone's "today" is included).
5. `/accounts/@name` is a client route. The Pages Function `functions/accounts/[username].ts` fetches the `/404.html` shell, calls RPC `get_public_profile`, and injects OG tags for public profiles.

## 8. Offline and caching

`platform/service-worker.ts`: precaches build and static files under `app-<version>`, cache first for `/_app/immutable/`, stale while revalidate for navigations (network failure serves the cached copy), cache first for the pinned Pyodide CDN cache `pyodide-v0.27.2`, deletes old caches on activate, uses `skipWaiting` and `clients.claim`.

## 9. Account deletion

`deleteAccount()`: revoke GitHub grant (POST `/api/github/disconnect`), call RPC `delete_my_account` (15 s timeout; deletes `auth.users` and cascades), `signOut`, remove every `trentorch*` localStorage key, then a full page reload so no signed in state survives in memory.
