# 07. Content Pipeline

## Authoring a question

Folder: `data/app_data/<NN-section>/<NN-track>/<NN-question>/` containing:

| File          | Content                                                                                                                                                             |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `README.md`   | Frontmatter (`name`, `title`, `tags`, `difficulty` in Beginner, Intermediate, Advanced, Mastery), then `## Statement`, `## Theory`, `## Explanation` in that order. |
| `starter.py`  | What the student starts with (also embedded in the Statement).                                                                                                      |
| `solution.py` | Reference solution; runs under real pytest in CI and in Pyodide in `test:pyodide`.                                                                                  |
| `tests.py`    | Pytest style tests. May call `load_solution("<section>/<track>/<question>/solution.py")` to reuse other solutions.                                                  |

POTD questions live in `99-potd/01-daily/` and are scheduled in `data/potd.ts`. A POTD is deliberately absent from `data/questions.ts`.

Numeric prefixes only set order. Ids drop the prefix (`stripNumericPrefix`); the raw names are kept as `sectionFolder`, `trackFolder`, `folder` for path lookups.

## Compile step

`node processes/curriculum-build/build.mjs` reads all sections, tracks and questions and writes `data/curriculum/generated-curriculum.json`. Any missing file or malformed README throws, so a bad question fails loudly. The JSON is committed. Nothing in `npm run build` regenerates it.

`generated-curriculum.spec.ts` checks the shape and the invariants.

## Turning a question into an IDE page

Build time (server load, once per page): `loadIdeContent(id)` finds the question in `questionsById`, `toQuestionContent` builds `QuestionContent`, including `testHarnessCode` from `buildTestHarness`.

Harness construction (`build-test-harness.ts`):

1. `stripLoadSolutionBoilerplate(tests)` removes the `load_solution` import and call statements, records which module aliases the tests use, and keeps pure attribute aliases.
2. `collectCleanedDependencies` walks the solutions the tests import, post order, with a cycle guard, so dependencies are defined before dependents.
3. `buildLoadSolutionShim` embeds those sources (base64) in a Python `load_solution` that runs each in an isolated `_Namespace`, so a student's code never shadows a dependency.
4. Output is two sections split by `STUDENT_CODE_MARKER`. Before it: dependencies, rebinds, shim. After it: bindings of the student's module names, the cleaned tests, and `TEST_COLLECTOR`.

Run time (`build-test-runner-script.ts`): `SETUP_SCRIPT`, then the pytest shim, then the first harness section, the sanitized student code (`sanitizeStudentCode`), then the second section. `TEST_COLLECTOR.run_tests(limit)` runs test functions, supports `tmp_path` only, and reports each result; an assert with no message reports the exception name.

Supported test features are intentionally small: `pytest.raises`, `tmp_path`, plain asserts. Anything else (fixtures, parametrize, monkeypatch) will not work in the browser and must not be used in `tests.py`. The slow suite (`npm run test:pyodide`) catches this by running every solution through the same harness in real Pyodide; documented exceptions live in `pyodide-check/known-failures.json`.

## Content tests

`npm run test:content` runs `python -m pytest data/app_data -q -n auto` with the pinned requirements. `pytest.ini` sets `python_files = tests.py` and importlib import mode so identically named test files in different folders do not collide.

## Guide pane rendering

`GuidePane.svelte` renders Description (Statement), Theory (with an optional simple version from `extractSimpleVersion`) and Solution. Markdown goes through `marked` plus `marked-katex-extension` (`$inline$` and `$$block$$` LaTeX), then DOMPurify before `{@html}`. POTD questions get reduced tabs as described in [02 flow 6](02-flows.md).
