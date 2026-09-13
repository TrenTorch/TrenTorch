# Repo reorg: data/ + processes/ + platform/

## Goal

Reorganize TrenTorch-Web's root so the repo reads as three clearly-separated top-level compartments: `data/` (curriculum content, untouched), `processes/` (feature logic, one function per file, grouped by feature), and `platform/` (everything that runs the website: routes, components, assets, static files).

## Architecture

SvelteKit's routing/lib conventions are directory-based but configurable via `svelte.config.js`'s `kit.files` block. Moving `src/routes` -> `platform/routes` and `src/lib` -> `platform/lib` (roughly) requires setting `kit.files.routes`, `kit.files.lib`, `kit.files.assets`, and `kit.files.appTemplate`/`kit.files.errorTemplate` if those exist, plus fixing every `$lib/...` and relative import across the codebase. `processes/` is new code-organization for existing logic — no framework awareness needed there, since it's imported by `platform/` code via relative or aliased paths, not a SvelteKit-special directory.

Two things are NOT literally splittable into one-function-per-file without breaking correctness, and this plan keeps them as single cohesive files with a one-line comment explaining why:
- `PyodideService` (a class managing a single Pyodide worker's lifecycle: init, exec, terminate) — splitting its methods into separate files would break encapsulation of its private state.
- The three Svelte reactive stores (`attempted`, `solved`, `collapsedSections`) — each is a single `$state`-backed object with closely-coupled getter/setter methods sharing one reactive closure; splitting would either duplicate the state or require awkward cross-file closures.
- `pyodideWorker.ts`'s top-level `self.onmessage` dispatch — a Web Worker needs exactly one entry file registered as the worker script. Its two genuinely independent helper functions (`initializePyodide`, `toBase64`) DO get extracted into their own files.

Everything else genuinely has independent, stateless functions and gets fully split.

## Tech stack

SvelteKit (adapter-static), TypeScript, Vite, Node (scripts/build-curriculum.mjs is plain Node/ESM, no TS).

## File mapping

### platform/ (from src/)

| From | To |
|---|---|
| `src/routes/**` | `platform/routes/**` (unchanged content) |
| `src/lib/components/**` | `platform/components/**` (unchanged content) |
| `src/lib/assets/**` | `platform/assets/**` |
| `src/lib/fonts/**` | `platform/fonts/**` |
| `src/lib/utils.ts` | `platform/lib/utils.ts` |
| `src/lib/index.ts` | `platform/lib/index.ts` |
| `src/lib/curriculum/types.ts` | stays at `src/lib/curriculum/types.ts` -- wait, see note below |
| `static/**` | `platform/static/**` |
| `src/app.html` | `platform/app.html` |
| `src/service-worker.ts` | `platform/service-worker.ts` |
| `src/app.d.ts` | stays at `src/app.d.ts` (ambient global types, not a SvelteKit `kit.files` path -- TypeScript just needs it included via `tsconfig.json`'s `include`, no framework-specific relocation needed; moving it is optional/cosmetic) |

Note on `src/lib/curriculum/`: user decided `generated-curriculum.json` stays "with data/". Since it's a build *output*, not source, and `types.ts` describes its shape, both move to `data/curriculum/` (generated-curriculum.json + types.ts), NOT under `platform/`. `data/app_data/` (the source `.py`/`.md` files) is untouched.

### processes/ (from src/lib and scripts/)

| From | To |
|---|---|
| `scripts/build-curriculum.mjs`'s `isDir` | `processes/curriculum-build/is-dir.mjs` |
| ...`readIfExists` | `processes/curriculum-build/read-if-exists.mjs` |
| ...`listContentDirs` | `processes/curriculum-build/list-content-dirs.mjs` |
| ...`stripNumericPrefix` | `processes/curriculum-build/strip-numeric-prefix.mjs` |
| ...`parseFrontmatterValue` | `processes/curriculum-build/parse-frontmatter-value.mjs` |
| ...`parseReadme` | `processes/curriculum-build/parse-readme.mjs` |
| ...`buildQuestion` | `processes/curriculum-build/build-question.mjs` |
| ...`buildTrack` | `processes/curriculum-build/build-track.mjs` |
| ...`buildSection` | `processes/curriculum-build/build-section.mjs` |
| ...`build` (entry, writes the JSON) | `processes/curriculum-build/build.mjs` (new entry point; `package.json`'s build script path updates to match) |
| `src/lib/content/ideContent.ts`'s `loadIdeContent` | `processes/ide-content/load-ide-content.ts` |
| ...`listIdeContentIds` | `processes/ide-content/list-ide-content-ids.ts` |
| ...`getAdjacentQuestionIds` | `processes/ide-content/get-adjacent-question-ids.ts` |
| ...shared internal shaping helpers + `GeneratedQuestion` interface | `processes/ide-content/shape-question-content.ts` (imported by the three files above) |
| `src/lib/runtime/pyodideService.ts`'s `sanitizeStudentCode` | `processes/code-execution/sanitize-student-code.ts` |
| ...`PyodideService` class + `pyodideService` instance | `processes/code-execution/pyodide-service.ts` (stays one file, see Architecture note) |
| `src/lib/runtime/pyodideWorker.ts`'s `initializePyodide` | `processes/code-execution/initialize-pyodide.ts` |
| ...`toBase64` | `processes/code-execution/to-base64.ts` |
| ...worker entry/dispatch | `processes/code-execution/pyodide-worker.ts` (stays one file, imports the two above) |
| `src/lib/runtime/storage.ts`'s `saveUserCode` | `processes/code-execution/save-user-code.ts` |
| ...`loadUserCode` | `processes/code-execution/load-user-code.ts` |
| ...`resetUserCode` | `processes/code-execution/reset-user-code.ts` |
| ...`loadIdeLayout` | `processes/code-execution/load-ide-layout.ts` |
| ...`saveIdeLayout` | `processes/code-execution/save-ide-layout.ts` |
| `src/lib/stores/attempted.svelte.ts` | `processes/progress-tracking/attempted.svelte.ts` (stays one file, see Architecture note) |
| `src/lib/stores/solved.svelte.ts` | `processes/progress-tracking/solved.svelte.ts` (stays one file) |
| `src/lib/stores/collapsedSections.svelte.ts` | `processes/progress-tracking/collapsed-sections.svelte.ts` (stays one file) |
| `src/lib/markdown.ts`'s `renderMarkdown` | `processes/markdown-rendering/render-markdown.ts` |

### data/ (mostly unchanged)

| From | To |
|---|---|
| `data/app_data/**` | unchanged |
| `src/lib/data/questions.ts` | `data/questions.ts` |
| `src/lib/data/questions.spec.ts` | `data/questions.spec.ts` |
| `src/lib/curriculum/generated-curriculum.json` | `data/curriculum/generated-curriculum.json` |
| `src/lib/curriculum/types.ts` | `data/curriculum/types.ts` |

### Stays at repo root, untouched

`package.json`, `svelte.config.js` (content updated, location unchanged -- SvelteKit requires this), `tsconfig.json`, `.config/vite.config.ts`, `.config/eslint.config.js`, `components.json`, `data/app_data/**`.

## Task breakdown

### Task 1: Move platform/ content, no logic changes

1. `git mv src/routes platform/routes`
2. `git mv src/lib/components platform/components`
3. `git mv src/lib/assets platform/assets`
4. `git mv src/lib/fonts platform/fonts`
5. `mkdir -p platform/lib && git mv src/lib/utils.ts platform/lib/utils.ts && git mv src/lib/index.ts platform/lib/index.ts`
6. `git mv static platform/static`
7. Update `svelte.config.js`:
   ```js
   kit: {
       files: {
           routes: 'platform/routes',
           lib: 'platform/lib',
           assets: 'platform/static',
           appTemplate: 'platform/app.html' // if app.html currently lives under src/
       },
       adapter: adapter({ fallback: '404.html' }),
       ...
   }
   ```
   Check first whether `src/app.html` exists (SvelteKit's default app template location) -- if so, `git mv src/app.html platform/app.html` and set `files.appTemplate` accordingly; if it lives elsewhere already, leave `files.appTemplate` unset.
8. Since `$lib` now resolves to `platform/lib`, every component under `platform/components/**` needs to move there too for `$lib/components/...` imports to keep working -- confirm this by checking `tsconfig.json`'s path aliases don't hardcode `src/lib`.
9. Fix every import across the moved files: run `grep -rl "\$lib/components\|\$lib/utils" platform/ ` and update paths where the move changed relative depth (imports using the `$lib` alias won't need path changes, only ones using relative `../../lib/...` paths will).
10. Verify: `npm run check` (0 errors expected), `npm run dev` and manually load `/`, `/questions`, `/ide/<any-slug>` in a browser.

### Task 2: Move data/ content (generated-curriculum.json, types.ts, questions.ts)

1. `mkdir -p data/curriculum && git mv src/lib/curriculum/generated-curriculum.json data/curriculum/generated-curriculum.json && git mv src/lib/curriculum/types.ts data/curriculum/types.ts`
2. `git mv src/lib/data/questions.ts data/questions.ts && git mv src/lib/data/questions.spec.ts data/questions.spec.ts`
3. Fix every import of `$lib/curriculum/generated-curriculum.json`, `$lib/curriculum/types`, `$lib/data/questions` across the codebase (these no longer resolve via `$lib` -- decide on a new alias, e.g. add `$data` in `tsconfig.json`'s `compilerOptions.paths` and `vite.config.ts`'s `resolve.alias`, pointing at `data/`). Update every consuming file (`platform/components/*`, `platform/routes/**`, and later `processes/ide-content/*`) to `import ... from '$data/curriculum/generated-curriculum.json'` etc.
4. Verify: `npm run check`, `node scripts/build-curriculum.mjs` (still at old location for now, Task 3 moves it) still writes to the new `data/curriculum/generated-curriculum.json` path -- update its output path constant accordingly.

### Task 3: Split scripts/build-curriculum.mjs into processes/curriculum-build/

1. `mkdir -p processes/curriculum-build`
2. Extract each function listed in the mapping table into its own file, each exporting exactly that one function (plus any small pure helper it exclusively uses). Preserve JSDoc/comments.
3. `processes/curriculum-build/build.mjs` becomes the new entry point: imports all the pieces, keeps the `build()` orchestration logic, writes to `data/curriculum/generated-curriculum.json`.
4. Update `package.json`'s script that currently runs `node scripts/build-curriculum.mjs` to point at `node processes/curriculum-build/build.mjs`.
5. `git rm scripts/build-curriculum.mjs` (or `rmdir scripts/` if nothing else lives there -- confirm first).
6. Verify: `node processes/curriculum-build/build.mjs` runs clean, output byte-identical (modulo path) to before, `npm run check`.

### Task 4: Split src/lib/content/ideContent.ts into processes/ide-content/

1. `mkdir -p processes/ide-content`
2. Move `GeneratedQuestion` interface + any private shaping helpers into `processes/ide-content/shape-question-content.ts`.
3. Extract `loadIdeContent`, `listIdeContentIds`, `getAdjacentQuestionIds` into their own files, each importing from `shape-question-content.ts` and `$data/curriculum/...` as needed.
4. `git rm src/lib/content/ideContent.ts` (and the now-empty `src/lib/content/` dir).
5. Update the 4 consumers found in `platform/routes/ide/[id]/+page.ts`, `+page.svelte`, and wherever else `$lib/content/ideContent` was imported, to import from the new `processes/ide-content/*` files (need a new alias, e.g. `$processes`, in `tsconfig.json`/`vite.config.ts`).
6. Verify: `npm run check`, load `/ide/<slug>` in dev server, confirm starter code and Solution tab still render.

### Task 5: Split src/lib/runtime/* into processes/code-execution/

1. `mkdir -p processes/code-execution`
2. `sanitizeStudentCode` -> `sanitize-student-code.ts`; `PyodideService` class + `pyodideService` singleton -> `pyodide-service.ts` (one file, importing `sanitize-student-code.ts`).
3. `initializePyodide` -> `initialize-pyodide.ts`; `toBase64` -> `to-base64.ts`; worker entry (the `self.onmessage` dispatch and whatever else remains) -> `pyodide-worker.ts`, importing both.
4. `saveUserCode`, `loadUserCode`, `resetUserCode`, `loadIdeLayout`, `saveIdeLayout` -> five separate files under `processes/code-execution/`.
5. `git rm -r src/lib/runtime/`.
6. Update the worker's registration path (wherever `new Worker(new URL('.../pyodideWorker.ts', import.meta.url))` or similar is instantiated -- check `pyodideService.ts` itself and any component that spins up the worker) to point at the new path.
7. Update every consumer (`platform/components/ide/*`, `platform/routes/ide/**`) to import from `processes/code-execution/*`.
8. Verify: `npm run check`, load `/ide/<slug>`, actually run a piece of code in the embedded editor (Pyodide worker round-trip), confirm code persistence (save/reload) still works.

### Task 6: Move src/lib/stores/* into processes/progress-tracking/

1. `mkdir -p processes/progress-tracking`
2. `git mv src/lib/stores/attempted.svelte.ts processes/progress-tracking/attempted.svelte.ts`
3. `git mv src/lib/stores/solved.svelte.ts processes/progress-tracking/solved.svelte.ts`
4. `git mv src/lib/stores/collapsedSections.svelte.ts processes/progress-tracking/collapsed-sections.svelte.ts`
5. `git rm -r src/lib/stores` (now empty)
6. Update every consumer (`platform/components/QuestionRow.svelte`, `ModuleSection.svelte`, `platform/routes/questions/+page.svelte`, `platform/routes/ide/[id]/+page.svelte`, etc. -- re-grep after Tasks 1-5 land since some of these will have already moved) to the new path.
7. Verify: `npm run check`, mark a question attempted/solved in dev server, reload, confirm persistence.

### Task 7: Move src/lib/markdown.ts into processes/markdown-rendering/ -- SKIPPED

`src/lib/markdown.ts` and its KaTeX wiring were part of earlier-session work that ended up in `git stash` (`stash@{1}`) and never actually landed on `main` -- the file does not exist on this branch. Nothing to move; task is a no-op until/unless that stash is resumed separately.

<!-- original task, preserved for when the stash is resumed:

1. `mkdir -p processes/markdown-rendering && git mv src/lib/markdown.ts processes/markdown-rendering/render-markdown.ts`
2. Update the one known consumer, `GuidePane.svelte` (now under `platform/components/ide/`), to the new import path.
3. Verify: `npm run check`, load `/ide/<slug>`, confirm the Description/Theory/Solution panes still render (including KaTeX math).
-->

### Task 8: Alias setup + final full verification

1. Confirm `tsconfig.json` and `.config/vite.config.ts` define exactly three aliases: `$lib` -> `platform/lib`, `$data` -> `data`, `$processes` -> `processes` (names open to bikeshedding, but something along these lines is needed since `processes/` and `data/` sit outside SvelteKit's default `$lib`).
2. `grep -rn "from '\.\./\.\./\.\./" platform processes` (or similar) to catch any leftover deep relative imports that should use an alias instead.
3. Full suite: `npm run check`, `npm run lint`, `npm run build`, `D:/Temp/claude/d--KC/956277ef-c540-4be7-9021-a5bb1cd5e054/scratchpad/torch-oracle-env/Scripts/python.exe -m pytest data/app_data -q` (should be unaffected -- confirms `data/app_data` truly wasn't touched).
4. `npm run dev`, manual smoke test: `/`, `/questions`, `/ide/<slug>` (load, run code, check Solution tab, mark solved, reload to confirm persistence), `/account`.
5. `git status` review -- confirm only intended files changed, `data/app_data/**` shows zero diff.

## Verification summary

- Zero changes to `data/app_data/**` (curriculum content untouched -- confirmed via `git diff --stat data/app_data` showing nothing).
- `npm run check` / `npm run lint` / `npm run build` all clean.
- Full pytest suite still 2761 passing (proves `data/app_data` wasn't touched).
- Manual smoke test of all 4 route types in a real browser.
