# 09. Testing, CI and Operations

## Commands

| Command                                     | Does                                                                                                                          |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `npm run dev` / `build` / `preview`         | Vite with `.config/vite.config.ts`. Dev server has no Functions, so GitHub sync shows `unavailable`.                          |
| `npm run check`                             | `svelte-kit sync` then `svelte-check`. Needs the two public Supabase env vars.                                                |
| `npm run lint`                              | Prettier check then eslint.                                                                                                   |
| `npm run format`                            | Prettier write.                                                                                                               |
| `npm test` / `test:unit`                    | Vitest project "server" (node env). Covers platform, processes, data and functions specs.                                     |
| `npm run test:content`                      | Python pytest over `data/app_data` with xdist. Needs `requirements-test.txt`.                                                 |
| `npm run test:pyodide`                      | Runs every authored solution in real Pyodide. Slow, needs network, downloads the numpy wheel. Timeouts 60 s test, 180 s hook. |
| `node processes/curriculum-build/build.mjs` | Regenerates the curriculum JSON. Run after any content change and commit the result.                                          |

## Unit test map

| Area                | Specs                                                                                                                            |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Functions           | `connection`, `crypto`, `github`, `profile-page`, `solution-files`, `api/github/sync`                                            |
| Content and harness | `generated-curriculum`, `build-test-harness`, `sanitize-student-code`, `pytest-shim`, `test-collector`, `extract-simple-version` |
| Data                | `questions`, `potd`                                                                                                              |
| Auth and profile    | `gate-behind-sign-in`, `preview-mode`, `prefill-from-account`, `validate-profile`                                                |
| POTD and rating     | `get-potd-part`, `potd-dates`, `rating-math`                                                                                     |
| SEO                 | `seo`                                                                                                                            |
| Pyodide             | `pyodide-check/questions.spec.ts`                                                                                                |

## GitHub workflows (`.github/workflows`)

These files were inherited from the public repo `TrenTorch/TrenTorch` through the mirror, so some comments say "this repo" for the public one. In the private repo, the ones that matter for shipping are CI and the security checks.

| Workflow                                                                                         | Trigger                    | Purpose                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------ | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ci.yml`                                                                                         | push and PR to main or dev | `npm ci`, lint, check, test, build. Node 22, 10 minute timeout, concurrency cancels superseded PR runs. Needs secrets `PUBLIC_SUPABASE_URL`, `PUBLIC_SUPABASE_ANON_KEY`. |
| `codeql.yml`                                                                                     | push, PR, weekly Monday    | CodeQL analysis, 30 minute timeout.                                                                                                                                      |
| `dependency-review.yml`                                                                          | PR                         | Dependency review action, 5 minutes.                                                                                                                                     |
| `scorecard.yml`                                                                                  | weekly Wednesday, push     | OpenSSF Scorecard, SARIF upload.                                                                                                                                         |
| `semantic-pr-title.yml`                                                                          | `pull_request_target`      | Enforces conventional PR titles.                                                                                                                                         |
| `check-ai-coauthor.yml`                                                                          | PR and push                | Fails on AI co-author trailers or "Generated with" footers.                                                                                                              |
| `mirror-to-website.yml`                                                                          | push to main (public repo) | Force pushes main to `Shashank-Tripathi-07/trentorch-website` using secret `WEBSITE_MIRROR_TOKEN`; fails loudly when the secret is missing.                              |
| `auto-label-issues.yml`, `auto-label-prs.yml` (`labeler.yml`)                                    | issues, PRs                | Keyword and changed file labels.                                                                                                                                         |
| `maintainer-badge.yml`                                                                           | PRs, issues                | Badges maintainer authored items.                                                                                                                                        |
| `changelog-backfill.yml`, `sync-pr-reviewers-to-issue.yml`, `remove-closed-items-from-board.yml` | PR and issue events        | Project bookkeeping.                                                                                                                                                     |
| `renew-interaction-limit.yml`                                                                    | monthly                    | Renews the collaborators only interaction limit before its 6 month expiry.                                                                                               |
| `update-contributors.yml` (`scripts/update_contributors.py`)                                     | nightly                    | Regenerates the contributor grid in README from GitHub data.                                                                                                             |

Action versions are pinned by commit sha. Every job sets `timeout-minutes` (3 to 30) except scorecard and update-contributors, which rely on defaults.

## Release flow

Public repo main, then mirror force push to the private repo, then Cloudflare Pages build preview, then merge deploys production. CI runs on the public repo. Cloudflare needs the Functions env vars listed in [01](01-system-design.md).

## Operational checklists

Add or edit a question: edit files in the question folder, `npm run test:content`, run the compile step, `npm test`, optionally `npm run test:pyodide`, commit the JSON with the sources.

Add a POTD: author the folder in `99-potd/01-daily`, add an entry to `data/potd.ts`, add the same row to `potd_schedule` in Supabase (not automatic), compile.

Change rating rules: change the SQL function first, then mirror in `rating-math.ts` and its spec.

Rotate `TOKEN_SECRET`: all stored GitHub tokens become undecryptable; users must reconnect (decrypt returns null, connection treated as gone).

Add a Function env var: update `functions/_lib/env.ts` and the Cloudflare project settings.

## Other files

`funding.json` (funding manifest, `.well-known/funding-manifest-urls` points to it), `maintainer_use/` (changelog notes), `docs/plans` and `docs/specs` (historical design docs).
