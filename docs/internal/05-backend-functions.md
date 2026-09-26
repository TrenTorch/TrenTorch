# 05. Backend: Cloudflare Pages Functions

Location: `functions/`. Runtime: Workers (Web Crypto, `fetch`, KV). Types in `_lib/env.ts`.

## Endpoints

| Route | Method | Auth | Purpose |
|-|-|-|-|
| `/api/github/start` | POST | Bearer Supabase JWT | Return the GitHub authorize URL with a signed state. |
| `/api/github/callback` | GET | signed `state` | Exchange the code, confirm app installation, store encrypted tokens, redirect to `/account`. |
| `/api/github/status` | GET | Bearer | Whether a usable connection exists, and the GitHub login. |
| `/api/github/sync` | POST | Bearer | Commit the solution files to the user's `trentorch-solutions` repo. |
| `/api/github/disconnect` | POST | Bearer | Revoke the GitHub grant and delete the stored connection. |
| `/accounts/[username]` | GET | none | Serve the `/404.html` shell with profile meta tags injected. |

Every handler except `callback` and `sync` is wrapped in `guard()`. `callback` and `sync` handle their own errors so they can redirect or return specific codes.

## `_lib` modules

| File | Functions |
|-|-|
| `env.ts` | Types `Env`, `PagesContext`, `PagesHandler`, `StoredConnection`, `KVNamespaceLike`. `REPO_NAME = 'trentorch-solutions'`. `connectionKey(userId)` returns `gh:<userId>`. `json(body, status)` sets `content-type` and `cache-control: no-store`. `readConnection(raw)` parses and validates stored JSON, null when malformed. `guard(handler)` catches every throw and returns `{error:'unavailable'}` with 502. |
| `auth.ts` | `verifiedUserId(request, env)`: reads the Bearer token, calls Supabase `/auth/v1/user` (8 s), returns the user id or null on any non-ok. Trusting Supabase to verify means no JWT secret lives here. |
| `crypto.ts` | `signState(userId, secret, now)` and `verifyState(...)`: HMAC-SHA256 over `userId` plus expiry, base64url, 10 minute TTL. `encryptToken(token, secret)` and `decryptToken(stored, secret)`: AES-GCM with a fresh random 12 byte IV per encryption, key = SHA-256 of `token:${secret}`; decrypt returns null on failure. Helpers `toBase64Url`, `fromBase64Url`, `hmacKey`, `aesKey`. |
| `github.ts` | `authorizeUrl`, `installUrl(slug, state)`, `exchangeCode`, `refreshTokens`, `getLogin`, `findRepoAccess(token, login)` (returns a tagged `RepoAccess`: installed with repo, not installed, and so on), `putFile`, `revokeGrant`. Internals: `call()` (8 s abort), `headers()`, `requestTokens()`, `isRateLimited()`. |
| `connection.ts` | `storeTokens(...)`: encrypts and writes to KV. `usableToken(...)`: returns a valid access token, refreshing when within 60 s of expiry, with the parallel rotation recheck and delete-on-failure described in [03](03-resilience.md). |
| `solution-files.ts` | `isSafeQuestionId`, `parseSolutionInput(body)`, `buildReadme(input)`, `solutionFiles(input)` (paths `solutions/<id>/solution.py` and `README.md`), `commitMessage(title)`, limits `MAX_CODE_LENGTH` and `MAX_DESCRIPTION_LENGTH`. |
| `profile-page.ts` | `PROFILE_PATH_PATTERN`, `escapeHtml` (numeric entities), `profileHead(profile, origin)` builds title, description, canonical and OG tags, `injectHead(shell, head)` inserts them into the HTML shell. |

## Handler details

`start.ts`: verify user, `signState`, return `{url}`.

`callback.ts`: verify state, `exchangeCode`, `getLogin`, `findRepoAccess`. Not installed and no `installation_id` in the query: redirect to `installUrl`. Not installed but `installation_id` present: stop with `/account?github=error` (loop guard). Installed: `storeTokens`, redirect `/account?github=connected`. Any throw: `/account?github=error`.

`status.ts`: `readConnection` from KV, returns connected flag and login; does not refresh.

`sync.ts` has its own try/catch instead of `guard` (any throw gives `github_failed` 502). Order of checks: verify user (401 `unauthorized`); declared `content-length` over 120,000 or body text over 120,000 gives 413 `invalid`; JSON parse plus `parseSolutionInput` (400 `invalid`); read and validate the KV connection (409 `not_connected`); repo is `stored.repo` or `<login>/trentorch-solutions`; `usableToken` (null gives 409); write files sequentially with `putFile`. Result mapping: `unauthorized` deletes the KV connection and gives 409 `not_connected`; `rate_limited` gives 429; `error` gives 502 `github_failed`. Success returns `{ok: true, changed}` where `changed` is true if any file was actually committed.

`status.ts`: reads KV and validates only. It returns `{connected: false}` or `{connected: true, login, repo}` and never refreshes tokens.

`disconnect.ts`: decrypt the stored token, `revokeGrant` at GitHub (result ignored), delete the KV key, return `{connected: false}`. Deletes even when decryption fails.

`accounts/[username].ts`: match `PROFILE_PATH_PATTERN`; fetch the shell via `ASSETS` or the origin; RPC `get_public_profile` (5 s); on success inject head and answer with `cache-control: public, max-age=60`; on any failure return the untouched shell with 200.

## Security properties

Tokens are encrypted at rest and never returned to the browser. OAuth state binds the flow to the user id and expires. Question ids are validated so a client cannot write outside `solutions/<id>/`. Refresh token rotation is race safe. Responses that carry user data are `no-store`. The Functions never run student code.
