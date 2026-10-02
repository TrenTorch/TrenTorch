# TrenTorch Website: Internal Documentation

Audience: engineers working on the private repo `Shashank-Tripathi-07/trentorch-website`, which deploys trentorch.com. This set is derived from the code, not from the older READMEs (several of those are stale, see [10-known-drift.md](10-known-drift.md)).

## Reading order

| File                                               | Contents                                                                                                                |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| [01-system-design.md](01-system-design.md)         | What the product is, the architecture, runtime components, build and deploy, environment                                |
| [02-flows.md](02-flows.md)                         | Step by step data flows: sign-in, progress sync, draft sync, code execution, GitHub sync, POTD and rating, SEO, offline |
| [03-resilience.md](03-resilience.md)               | Every timeout, retry, debounce, limit, fallback and idempotency rule in one place                                       |
| [04-file-reference.md](04-file-reference.md)       | Every directory and file, with a description of every function                                                          |
| [05-backend-functions.md](05-backend-functions.md) | Cloudflare Pages Functions: endpoints, storage, crypto, error codes                                                     |
| [06-database.md](06-database.md)                   | Supabase schema, RLS, RPCs, rating math                                                                                 |
| [07-content-pipeline.md](07-content-pipeline.md)   | How a question is authored, built, tested and executed in the browser                                                   |
| [08-frontend.md](08-frontend.md)                   | Routes, layout, components, state stores, styling                                                                       |
| [09-ci-testing-ops.md](09-ci-testing-ops.md)       | Tests, scripts, GitHub workflows, mirror flow, funding manifest                                                         |
| [10-known-drift.md](10-known-drift.md)             | Stale docs, gaps, and inconsistencies found while writing this                                                          |

## One paragraph summary

TrenTorch is a free, browser-only ML practice site. About 340 curated questions (plus a daily Problem of the Day) are compiled at build time into a static SvelteKit site. Python runs in a Pyodide web worker in the visitor's browser, so there is no code execution server. Accounts, progress, drafts, ratings and profiles live in Supabase, accessed straight from the browser under row level security. A small set of Cloudflare Pages Functions handles the one thing that needs a secret: saving accepted solutions to the user's own GitHub repository through a GitHub App, plus server-injected meta tags for public profile links.

## Glossary

| Term                 | Meaning                                                                                                                    |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Part                 | Top level curriculum section (20 of them), e.g. `part-python`.                                                             |
| Track                | Ordered group of questions inside a Part.                                                                                  |
| Question / slug / id | One problem. The slug is the URL segment `/ide/<slug>` and the key in every store.                                         |
| POTD                 | Problem of the Day. Scheduled in `data/potd.ts`, lives under `data/app_data/99-potd/01-daily`, not in the curriculum list. |
| Run                  | Execute against the first 2 sample tests. Never records progress.                                                          |
| Submit               | Execute the full hidden suite. Marks attempted, and solved if all pass.                                                    |
| Solved               | Earned only by a passing Submit. Never granted by the client on its own.                                                   |
| Attempted            | A Submit ran, pass or fail.                                                                                                |
| Draft                | Editor contents for a question, saved locally and synced to Supabase when signed in.                                       |
| Harness              | The generated Python that wraps the student code plus tests for Pyodide.                                                   |
| Connection           | The stored GitHub OAuth tokens for one user in Cloudflare KV.                                                              |
