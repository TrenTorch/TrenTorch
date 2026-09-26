# 04. File and Function Reference

Grouped by directory. Spec files (`*.spec.ts`) sit beside the module they test and are listed in [09](09-ci-testing-ops.md). Backend functions are described in more depth in [05](05-backend-functions.md), the database in [06](06-database.md).

## Root and config

| File | Purpose |
|-|-|
| `package.json` | Scripts (dev, build, preview, check, lint, format, test, test:unit, test:content, test:pyodide), prettier config, deps. |
| `svelte.config.js` | adapter-static with `fallback: '404.html'`; `kit.files` remapped to `platform/`; aliases `$data $processes $components $assets $fonts`; forces runes. |
| `.config/vite.config.ts` | Tailwind v4 plugin, SvelteKit plugin, manual chunk `codemirror`, vitest project "server" (node env, includes platform, processes, data, functions specs). |
| `.config/vitest.pyodide.config.ts` | Config for the slow real-Pyodide suite (60 s test, 180 s hook timeouts). |
| `.config/eslint.config.js` | eslint 10 with svelte rules (includes `svelte/no-navigation-without-resolve`). |
| `tsconfig.json`, `components.json` | TS paths and shadcn-svelte settings (style nova). |
| `.env.example` | Public Supabase variables. |
| `.nvmrc`, `.npmrc` | Node 24.19.0, `engine-strict=true`. |
| `vercel.json` | `{"git":{"deploymentEnabled":false}}`; Vercel is not used to deploy this repo. |
| `funding.json` | FLOSS/fund funding manifest (schema 1.1.0); also `.well-known/funding-manifest-urls`. |
| `src/app.d.ts` | Global SvelteKit types. |
| `platform/app.html` | HTML shell: pre-hydration theme script (reads `theme` from localStorage), preconnect to cdn.jsdelivr.net, `data-sveltekit-preload-data="hover"`. |
| `platform/service-worker.ts` | See [02 section 8](02-flows.md). |

## data/

| File | Contents and functions |
|-|-|
| `data/questions.ts` | Curated curriculum. Types `Difficulty` (Easy, Medium, Hard), `CompanyTag`, `Question`, `Track`, `Part`. `slugify(title)` builds a slug. `mkTrack(name, topics, rows)` builds a track from `[title, difficulty, explicitSlug?]` tuples. `withCompanies(part, tag)` attaches company tags to every question. `COMPANY_TAGS` maps Parts to companies and roles. `curriculum` (20 Parts, see list below). `getProgressStats(solved)` returns completed and total (intersected with real slugs so renamed slugs never inflate counts). `getInProgressCount(solved, attempted)`. `getPartProgress(solved)` per Part. `getDifficultyProgress(solved)` per difficulty. `findQuestionBySlug(slug)` returns the question with its Part and Track. |
| `data/potd.ts` | `PotdEntry` (date, questionId, difficulty) and `potdEntries`, 39 entries from 2026-09-14 to 2026-10-22. Must be mirrored by hand into `potd_schedule` in Supabase. |
| `data/faq.ts` | `FaqEntry`, `FAQ_DISCLAIMER`, `buildFaqEntries(questionCount)`. Feeds both the FAQ page and its JSON-LD. |
| `data/part-icons.ts` | `getPartIcon(partId)` returns a lucide icon; fallback `Gauge`. The three newest Parts have no mapping. |
| `data/curriculum/types.ts` | `QuestionMetadata`, `QuestionContent` (id, metadata, descriptionMarkdown, theoryMarkdown, solutionCode, starterCode, testHarnessCode), `SingleTestResult`, `SubmissionResult`, `RuntimeState`, `ExecutionResult`. |
| `data/curriculum/generated-curriculum.json` | Build artifact of `build.mjs`. Never hand edited. About 11k lines. |
| `data/app_data/` | Authored content. Section folders `00-python` to `16-production-and-advanced-ai-systems` plus `99-potd/01-daily`. Each question folder has `README.md, starter.py, solution.py, tests.py`. Support files: `_load.py` (`load_solution(relpath)` imports a solution under a unique module name), `pytest.ini` (`python_files = tests.py`, importlib import mode), `requirements-test.txt` (numpy 2.5.3, scikit-learn 1.9.1, torch 2.14.0+cpu, pytest 9.1.1, pytest-xdist 3.8.0). |

The 20 Part ids: part-python, part-numpy, part-math, part-data-foundations, part-classical-linear, part-classical-trees, part-classical-unsupervised, part-dl-core, part-dl-training, part-seq-modeling, part-transformers-llm, part-vision, part-systems-perf, part-systems-distributed, part-rl-alignment, part-production-ml, part-inference, part-agentic-systems-and-orchestration, part-reliability-safety-and-evaluation, part-production-and-advanced-ai-systems.

## processes/auth

| File | Function |
|-|-|
| `supabase-client.ts` | `getSupabaseClient()`: lazy singleton, browser only. |
| `session.svelte.ts` | `session` (reactive `user`, `accessToken`, loading), `signInWithGitHub`, `signInWithGoogle`, `signInWithMagicLink(email)`, `signOut`, internal `redirectTo`. |
| `gate-behind-sign-in.ts` | `gateBehindSignIn(event)`: intercepts plain clicks on gated links when signed out. |
| `after-sign-in-destination.ts` | `rememberAfterSignInDestination(path)`, `clearAfterSignInDestination()`, `takeAfterSignInDestination()` (returns and clears; only same-site paths). |
| `sign-in-prompt.svelte.ts` | `signInPrompt` with `open(reason)` and `close()`; reason `'run'` or `'browse'`. |
| `preview-mode.ts` | `signInSkipped()`: true when `VITE_PREVIEW_SKIP_SIGN_IN=1`. |
| `delete-account.ts` | `deleteAccount()` (see flow 9) and internal `clearLocalData()`. |

## processes/code-execution

| File | Function |
|-|-|
| `pyodide-service.ts` | `PyodideService` singleton `pyodideService`: `init()`, `runCode(code)`, `runTests(code, harness, id, limit?)`, request map with timeouts, stores `runtimeState`, `consoleOutput`, `testResults`, `isRunning`. Kept as one class because the worker lifecycle state is private. |
| `pyodide-worker.ts` | Worker entry. One `onmessage` dispatch (init, run, test), origin check, posts results. |
| `initialize-pyodide.ts` | `initializePyodide()`: dynamic import of Pyodide 0.27.2 from jsDelivr, `loadPyodide`, preload numpy. |
| `pyodide-setup-script.ts` | `SETUP_SCRIPT` Python prelude (includes `OutputCapture`, the globals ordering workaround). |
| `build-test-runner-script.ts` | `buildTestRunnerScript(options)`: composes setup script, student code and harness sections into one script. |
| `pytest-shim.ts` | `PYTEST_SHIM`: fake `pytest` module that supports only `pytest.raises`. |
| `sanitize-student-code.ts` | `sanitizeStudentCode(code)`: removes dev only header lines (using `isBoilerplateStart` and `parenDelta` to track multi line statements). |
| `to-base64.ts` | `toBase64(str)`: UTF-8 safe base64 for embedding sources. |
| `save-user-code.ts`, `load-user-code.ts`, `reset-user-code.ts` | Editor code in localStorage under `trentorch_code_<id>` (`CODE_KEY_PREFIX` in `code-storage-key.ts`); save also stamps and queues a push; reset clears local and remote. |
| `ide-layout-key.ts`, `load-ide-layout.ts`, `save-ide-layout.ts` | `IdeLayout` (left pane percent, bottom pane percent) under `trentorch_ide_layout`, with defaults and try/catch. |
| `draft-sync.svelte.ts` | `draftSync` (reactive `version`, `wasPulled(id)`), `stampLocalDraft`, `forgetLocalDraftStamp`, `queueDraftPush`, `removeRemoteDraft`, `syncDrafts(userId)`, internal `readLocalTimestamp`, `readLocalDrafts`, `localAsDraft`, `runSync`. |

## processes/ide-content

| File | Function |
|-|-|
| `curriculum-index.ts` | Types `GeneratedQuestion` and section and track shapes; `questionsById` and `questionsByFullPath` maps built from the generated JSON at module load. |
| `load-ide-content.ts` | `loadIdeContent(id)` returns `QuestionContent` or null. |
| `to-question-content.ts` | `toQuestionContent(question)`: maps a generated question to page content (extracts starter code, builds harness). |
| `extract-starter-code.ts` | `extractStarterCode(statementMarkdown)`: pulls the fenced starter from the Statement section. |
| `extract-simple-version.ts` | `extractSimpleVersion(theory)`: pulls the plain language section of the Theory text, or null. |
| `collapse-signatures.ts` | `collapseSignatures(code)`: collapses multi line function signatures so parsing is line based. |
| `build-test-harness.ts` | `buildTestHarness(question)`: builds the two section harness split at `STUDENT_CODE_MARKER`; before the marker: dependency solutions, renamed import rebinds, `load_solution` shim; after: module bindings, cleaned tests, `TEST_COLLECTOR`. Internal `isolatedSolutionSource`. |
| `collect-cleaned-dependencies.ts` | `collectCleanedDependencies(...)`: post order walk of solutions a test imports, with a `visiting` set to break cycles. |
| `strip-load-solution-boilerplate.ts` | `stripLoadSolutionBoilerplate(testsCode)`: removes `load_solution` calls and reports module aliases; helpers `loadCallTail`, `moduleAliasPairs`, `isPureModuleAttributeAlias`, `stripOuterParens`. |
| `load-solution-shim.ts` | `buildLoadSolutionShim(sourcesByPath)`: emits a Python `load_solution` that executes base64 embedded sources in isolated `_Namespace` objects. |
| `test-collector.ts` | `TEST_COLLECTOR` Python: `run_tests(limit)`, supports `tmp_path` only, an empty assert message falls back to the exception name. |
| `harness-marker.ts` | `STUDENT_CODE_MARKER = '# __student_code_runs_here__'`. |
| `get-adjacent-question-ids.ts` | `getAdjacentQuestionIds(id)`: previous and next slug in curriculum order. |
| `list-ide-content-ids.ts` | `listIdeContentIds()`: all authored ids. |

## processes/curriculum-build (node, `.mjs`)

| File | Function |
|-|-|
| `build.mjs` | `build()`: walks `data/app_data`, writes the JSON. Run with `node processes/curriculum-build/build.mjs`. |
| `build-section.mjs` | `buildSection(dirName, dirPath)`. |
| `build-track.mjs` | `buildTrack(sectionId, sectionDirName, trackDirName, trackDirPath)`. |
| `build-question.mjs` | `buildQuestion(...)`: reads README, starter, solution, tests; throws on any missing file. |
| `parse-readme.mjs` | `parseReadme(raw, questionDirPath)`: frontmatter plus `## Statement`, `## Theory`, `## Explanation` in order; throws when malformed. |
| `parse-frontmatter-value.mjs` | `parseFrontmatterValue(raw)`. |
| `strip-numeric-prefix.mjs` | `stripNumericPrefix(dirName)`: `03-foo` becomes `foo` for ids. |
| `list-content-dirs.mjs`, `is-dir.mjs`, `read-if-exists.mjs` | Filesystem helpers. |

## processes/progress-tracking

| File | Function |
|-|-|
| `solved.svelte.ts` | `solved`: `slugs`, `isSolved`, `markSolved`, `unmarkSolved`, `markSolvedFromRemote`; localStorage `trentorch-solved-questions`. |
| `attempted.svelte.ts` | `attempted`: same shape (`markAttempted`, `unmarkAttempted`, `markAttemptedFromRemote`). |
| `collapsed-sections.svelte.ts` | `collapsedSections.toggle(partId)`; `trentorch-collapsed-parts`. |
| `supabase-solved-store.ts` | `fetchSolvedQuestions(userId)`, `upsertSolvedQuestion`, `upsertSolvedQuestions`, `deleteSolvedQuestion`, `fetchSolvedDates(userId)` (for the contribution graph). |
| `supabase-drafts-store.ts` | `fetchDraftMeta`, `fetchDraftCodes`, `upsertDrafts` (uses `chunkDrafts`), `deleteDraft`, `fetchAttempted`, `upsertAttempted`, `deleteAttempted`. |
| `supabase-potd-attempts-store.ts` | `recordPotdAttempt(id, passed, total, allPassed)`: calls RPC `record_potd_attempt`. |
| `sync-solved-with-supabase.ts`, `sync-attempted-with-supabase.ts` | Two way union sync. |

## processes/potd, processes/rating

| File | Function |
|-|-|
| `potd/get-todays-potd.ts` | `getTodaysPotd(summaries)`: the entry whose date equals the local date. |
| `potd/get-potd-part.ts` | `getTodaysPotdPart`, `getPastPotdPart`: shape entries as Part and Track for `ModuleSection`. Internal `resolveEntries`. |
| `potd/potd-summary.ts` | `toPotdSummary(question)`: the few fields a client needs. |
| `potd/to-display-question.ts` | `toDisplayQuestion(summary, date)`, `parseLocalDateString`, `humanize`. |
| `potd/is-potd-question.ts` | `isPotdQuestion(id)`. |
| `potd/local-date-string.ts` | `localDateString(date)`: `YYYY-MM-DD` in local time. |
| `rating/rating-math.ts` | `expectedSolveProbability`, `applyPotdOutcome`, `tierForRating`, `qualifiesForInterviewReferral`; constants and `RATING_TIERS`. Mirrors the SQL. |
| `rating/rating-store.svelte.ts` | `ratingStore.setRating`, `clear`. |
| `rating/supabase-rating-store.ts` | `recordPotdOutcome` (RPC), `recordPotdAttempt` (upsert), `fetchUnratedPastAttempts`, `fetchRatingHistory`. |
| `rating/settle-past-potd.ts` | `settlePastPotdOutcomes(userId)`. |

## processes/profile, github-sync, seo

| File | Function |
|-|-|
| `profile/validate-profile.ts` | `ProfileForm`, `LIMITS`, `normalizeUsername`, `normalizeLink(kind, input)`, `validateProfile(form)`. |
| `profile/profile-store.ts` | `loadProfile(userId)`, `saveProfile(userId, form)` with 15 s timeouts. |
| `profile/public-profile.ts` | `fetchPublicProfile(username)` via RPC; returns `ViewedProfile`, null (missing or private) or undefined (error). |
| `profile/prefill-from-account.ts` | `prefillFromAccount(...)`: seeds a new profile from OAuth metadata. |
| `profile/profile-state.svelte.ts` | Shared reactive `profileState`. |
| `github-sync/github-sync.svelte.ts` | `githubSync` state, `loadGithubStatus`, `confirmFreshConnection`, `connectGithub`, `disconnectGithub`, `syncSolutionToGithub`, `resetGithubSync`; internals `authHeaders`, `request`, `pushOnce`. |
| `seo/site.ts` | Constants: `SITE_URL`, `SITE_NAME`, `GITHUB_URL`, OG image path and size, logo path. |
| `seo/absolute-url.ts`, `truncate.ts`, `with-site-name.ts`, `escape-xml.ts`, `to-json-ld-script.ts` | Small helpers (truncate to 160 for descriptions). |
| `seo/build-site-json-ld.ts`, `build-question-seo.ts`, `build-part-seo.ts`, `build-breadcrumb-json-ld.ts`, `build-faq-json-ld.ts` | JSON-LD and meta builders (Organization, WebSite, LearningResource, Course, CollectionPage, BreadcrumbList, FAQPage). |
| `seo/list-sitemap-paths.ts`, `build-sitemap-xml.ts`, `latest-live-date.ts`, `find-question-location.ts` | Sitemap generation. |

## functions/

See [05](05-backend-functions.md).

## platform/

Routes and components are described in [08](08-frontend.md). `platform/lib/utils.ts` has `cn(...)` (clsx plus tailwind-merge) and shadcn helper types. `platform/lib/vitest-examples/greet.ts` is a template leftover.

## supabase/, pyodide-check/, docs/, .github/

`supabase/migrations/` see [06](06-database.md). `pyodide-check/questions.spec.ts` runs every authored solution in Pyodide, with `known-failures.json` as the allow list. `docs/plans` and `docs/specs` hold the questions page spec and the repo reorganization plan (historical). `.github` see [09](09-ci-testing-ops.md).
