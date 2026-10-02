# 01. System Design

## Goals and shape

1. Serve every page as a static file from Cloudflare's edge (prerendered, no SSR at request time).
2. Run student code with no server: Pyodide in a web worker.
3. Keep secrets out of the browser. The only secrets belong to the GitHub App and live in Cloudflare Pages Functions.
4. Treat the network as unreliable. Local storage is the source of truth for the moment, Supabase is the cross device copy, and every remote write is fire and forget with timeouts.

## Architecture

```
                Browser (SvelteKit SPA hydrated from prerendered HTML)
  +=================================================================================+
  |  Routes + components (Svelte 5 runes)     Stores ($state, localStorage backed)  |
  |  CodeMirror 6 editor                      solved, attempted, collapsedSections  |
  |  Service worker (precache + SWR)          session, ratingStore, profileState    |
  |                                                                                 |
  |  Pyodide Web Worker  <= postMessage =>    PyodideService (main thread)          |
  +=========+====================+========================+=========================+
            |                    |                        |
            | supabase-js        | fetch /api/github/*    | dynamic import
            | (anon key + RLS)   | (Bearer Supabase JWT)  | cdn.jsdelivr.net
            v                    v                        v
   Supabase project        Cloudflare Pages Functions    jsDelivr CDN
   axgzkiqhelozgouszgex    functions/api/github/*        Pyodide 0.27.2 + wheels
   Auth, Postgres, RPCs    functions/accounts/[username]
                                 |
                                 +=> Supabase /auth/v1/user (verify JWT)
                                 +=> Supabase RPC get_public_profile
                                 +=> Cloudflare KV GITHUB_TOKENS (encrypted tokens)
                                 +=> api.github.com and github.com/login/oauth
```

Key decisions and their reasons:

| Decision                                                            | Reason                                                                                                                                                                               |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| adapter-static with `fallback: '404.html'`, everything prerendered  | No per request compute cost, search engines get real HTML with 200 status.                                                                                                           |
| Server `load` (not universal) for `/ide/[id]`, `/`, `/potd`, `/faq` | Universal loads re-run in the browser and would ship the ~4 MB curriculum to every visitor. Server loads run once at build and are written into the HTML and a static `__data.json`. |
| `/accounts/@name` not prerendered, served by a Pages Function       | The username is unknown at build time. The function injects OG and meta tags into the shell so shared links preview correctly.                                                       |
| Pyodide in a worker                                                 | Isolation from the UI thread, and `terminate()` on timeout kills runaway code.                                                                                                       |
| Supabase called directly from the browser                           | RLS plus column grants and SECURITY DEFINER RPCs enforce access, so no API server is needed.                                                                                         |
| GitHub sync through a Function                                      | The GitHub App client secret and the token encryption key cannot live in the browser.                                                                                                |
| Solved and rating are server computed for POTD                      | Clients cannot write `profiles.user_rating` (update revoked). The RPC does the math.                                                                                                 |

## Repository layout

| Path                   | Role                                                                                                                                                                        |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data/`                | Content and data: curated curriculum (`questions.ts`), POTD schedule (`potd.ts`), FAQ, part icons, authored question folders (`app_data/`), generated JSON (`curriculum/`). |
| `processes/`           | Feature logic grouped by domain, one function per file where practical. No SvelteKit specifics.                                                                             |
| `platform/`            | Everything that runs the site: `routes/`, `components/`, `lib/`, `service-worker.ts`, `app.html`, static assets and fonts. SvelteKit `kit.files` is remapped to it.         |
| `functions/`           | Cloudflare Pages Functions (`/api/github/*`, `/accounts/[username]`) and shared `_lib/`.                                                                                    |
| `supabase/migrations/` | SQL migrations 2026-09-22 to 2026-09-25.                                                                                                                                    |
| `pyodide-check/`       | Slow test that runs every authored solution in real Pyodide.                                                                                                                |
| `.config/`             | `vite.config.ts`, `vitest.pyodide.config.ts`, `eslint.config.js`.                                                                                                           |
| `.github/`             | Workflows, labeler, contributor script (inherited from the public repo, see [09](09-ci-testing-ops.md)).                                                                    |
| `docs/`                | Plans and specs from earlier work, plus this folder.                                                                                                                        |

Import aliases: `$data`, `$processes`, `$components`, `$assets`, `$fonts`, `$lib` (= `platform/lib`), plus SvelteKit's `$app/*`.

## Tech stack

SvelteKit 2, Svelte 5 with runes forced on by `vitePlugin.compilerOptions.runes`, TypeScript, Tailwind v4, shadcn-svelte (style "nova", components in `platform/components/ui`), layerchart, CodeMirror 6 (own chunk `codemirror`), marked plus marked-katex-extension plus KaTeX, DOMPurify, Pyodide 0.27.2, supabase-js, Cloudflare Pages Functions and KV, vitest, eslint 10, prettier (tabs, single quotes, width 100). Node 24.19.0 (`.nvmrc`, `engine-strict=true`).

## Build and deploy

1. The curriculum compile is a separate manual step: `node processes/curriculum-build/build.mjs` writes `data/curriculum/generated-curriculum.json`, which is committed (marked generated in `.gitattributes`). No npm script runs it, so after editing anything under `data/app_data/` you must run it and commit the result. Then `npm run build` (plain `vite build`) prerenders every route and every `/ide/<slug>` (entries from the curriculum plus all authored questions), every `/questions/<partId>`, and `sitemap.xml`.
2. Output in `build/` (static files, `404.html` used as SPA fallback for unprerendered routes such as `/accounts/@name`).
3. Cloudflare Pages deploys `build/` and the `functions/` directory. This repo's `vercel.json` only disables Vercel git deployments (`{"git":{"deploymentEnabled":false}}`).
4. Preview and release flow: pushes to the public repo are mirrored to this private repo (force push, see [09](09-ci-testing-ops.md)); Cloudflare previews the private repo and merging deploys production.

The public OSS build (Vercel project `trentorch-web-oss`) is a different app from this repo; it uses `buildCommand: "npm run build && cp build/404.html build/app.html"` plus a rewrite of `/(.*)` to `/app.html`.

## Environment and secrets

| Name                                                          | Where                                | Purpose                                                                                                 |
| ------------------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| `PUBLIC_SUPABASE_URL`, `PUBLIC_SUPABASE_ANON_KEY`             | build time, browser (`.env.example`) | Supabase client. Build and `svelte-check` fail without them because they are static public env imports. |
| `VITE_PREVIEW_SKIP_SIGN_IN=1`                                 | preview builds                       | `signInSkipped()` returns true so reviewers can run code without signing in.                            |
| `GITHUB_TOKENS`                                               | Pages KV binding                     | Encrypted GitHub tokens, key `gh:<userId>`.                                                             |
| `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`                    | Pages secret                         | GitHub App OAuth.                                                                                       |
| `GITHUB_APP_SLUG`                                             | Pages var                            | Builds the install URL.                                                                                 |
| `TOKEN_SECRET`                                                | Pages secret                         | Derives the HMAC key (OAuth state) and the AES key (token encryption).                                  |
| `PUBLIC_SUPABASE_URL`, `PUBLIC_SUPABASE_ANON_KEY` (Functions) | Pages                                | Used by `auth.ts` and the profile page function.                                                        |
| `ASSETS`                                                      | Pages binding, optional              | Static asset fetcher used to load the `/404.html` shell.                                                |

## Runtime components at a glance

| Component      | Lives in                                                                                                                 | Job                                                                                                                            |
| -------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| Root layout    | `platform/routes/+layout.svelte`                                                                                         | Navbar, footer (home only), and four invisible workers: `SignInDialog`, `ProgressSync`, `RatingSettle`, `AfterSignInRedirect`. |
| PyodideService | `processes/code-execution/pyodide-service.ts`                                                                            | Owns the worker, run and test requests, timeouts, state stores.                                                                |
| Stores         | `processes/progress-tracking/*.svelte.ts`, `processes/auth/session.svelte.ts`, `processes/rating/rating-store.svelte.ts` | Reactive state persisted to localStorage and mirrored to Supabase.                                                             |
| Sync engines   | `sync-*-with-supabase.ts`, `draft-sync.svelte.ts`, `github-sync.svelte.ts`                                               | Reconcile local and remote state.                                                                                              |
| Service worker | `platform/service-worker.ts`                                                                                             | Offline shell and CDN caching.                                                                                                 |
| Functions      | `functions/`                                                                                                             | GitHub OAuth, solution commits, profile meta tags.                                                                             |
