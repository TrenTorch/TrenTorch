# Curriculum Content — Authoring Guide

This is the source of truth for the atomized web curriculum (theory + question + tests + oracle solution, per topic). It is **authored here as real files**, and compiled in memory by `processes/curriculum-build/build.mjs` into the virtual modules the SvelteKit app imports (`virtual:curriculum/bundle` and `virtual:curriculum/catalogue`). Nothing generated is stored in the repo: edit the source files here and the dev server picks the change up.

This mirrors the pattern the TrenTorch CLI repo already uses: `data/src/<NN>/<NN>.py` (real, authored source) → `tren dev export` → the generated `trentorch` package. Same idea here: author in real `.py`/`.md` files, generate the final bundle as a build artifact.

## Why not one big JSON per question

Test code and oracle solutions are real Python. Stuffing multi-line Python inside a JSON string means no syntax highlighting while writing it, ugly single-line diffs in review, and no way to just run `pytest` on a question to confirm the oracle solution actually passes its own tests before it ever reaches the app. Real `.py` files fix all three.

## Why one README.md instead of meta.json + statement.md + theory.md + explanation.md

Earlier this content was four separate files per question (`meta.json`, `statement.md`, `theory.md`, `explanation.md`). In practice that meant opening four tabs to read one question end to end, and a metadata-only change (fixing a tag) sat in its own file next to prose it had nothing to do with. A single `README.md` — frontmatter for the structured fields, then the three markdown sections in reading order — is both the file a human opens first when browsing the folder in GitHub and the one file `processes/curriculum-build/build.mjs` needs to parse for everything but the code. `starter.py`, `solution.py` and `tests.py` stay separate real `.py` files (the reasoning above still applies to those).

## Folder structure

```
data/
  app_data/                      compiled curriculum content (this folder)
    _load.py                     shared, curriculum-wide test-only helper (see below)
    01-<root>/                   one of the 11 root tracks, e.g. 01-python, 02-mathematics, 04-classical-ml, 06-language-models
      meta.json                  {"title": "Python for Engineers"}: what the app shows for this folder
      01-<section>/              e.g. 01-supervised-models, 02-unsupervised-learning
        meta.json                {"title": "Supervised Models"}
        01-<track>/              the sub-section, e.g. 01-linear-regression, 02-classification
          meta.json              {"title": "Linear Regression"}
          01-<question-slug>/
            README.md            frontmatter (name, tags, difficulty) + ## Statement / ## Theory / ## Explanation
            starter.py           what the student actually sees first: real signature/docstring, body replaced with TODO + pass
            solution.py          the oracle solution — real, runnable Python
            tests.py             real pytest file, runnable directly: `pytest tests.py`
          02-<question-slug>/
            ...
  user_data/                     schema for what the app persists client-side — see data/user_data/README.md
```

`starter.py` exists because a student opening a question needs something to actually _do_ — `solution.py` alone is the finished answer with nothing left to implement. `starter.py` keeps the exact same function signature and docstring as `solution.py`, with the body replaced by a short `# TODO` comment (pointing back at Theory, never restating the formula) and a bare `pass`. It is never executed as-is; it exists purely as the starting point handed to a student in the IDE.

Numeric prefixes (`01-`, `02-`, ...) exist at all four levels -- root, section, track, and question -- purely to fix display/build order. Plain alphabetical folder sort put "classification" before "linear-regression" (wrong pedagogically: Linear Regression teaches the training-loop pattern every later track assumes) and "systems-optimization" before "vision-transformer" (wrong for the same reason, one level up). The prefix is build-order only, not part of the identity: `processes/curriculum-build/build.mjs` strips it before exposing `id`/`section`/`track`, so the compiled output and every cross-question reference still use the clean name (`classical-ml`, `linear-regression`), never the numbered folder name. Section and track directory names (after stripping the prefix) are kebab-case and match the `tags` used inside each question's `README.md` frontmatter.

## `README.md` schema

```markdown
---
name: linear-regression-hypothesis-function
title: Hypothesis Function
tags: [classical-ml, linear-regression, forward-pass]
difficulty: Beginner
---

## Statement

Problem description — the contract only, never the formula/one-liner answer.

## Theory

The theory, building on the previous question in the track.

## Explanation

Why the oracle solution is written this specific way.
```

The frontmatter block is a small fixed subset of YAML (plain scalars plus one `[a, b, c]` flow sequence for `tags`) parsed by hand in `processes/curriculum-build/build.mjs` — not a general YAML parser, so keep values plain. `difficulty` is one of `Beginner`, `Intermediate`, `Advanced`, `Mastery`. The three `##` sections must appear in exactly that order (Statement, then Theory, then Explanation) — the build fails loudly if one is missing or out of order, rather than silently shipping a blank tab in the IDE.

## Reusing an earlier question's solution in a later question's tests

Every question folder's solution file is named `solution.py` — the same name in every folder on purpose (keeps each question self-contained and easy to find). That means they can't all be imported with a plain `import solution` from the same test run without colliding.

**One shared `data/app_data/_load.py` for the entire curriculum.** A question never names where it lives, so folders can be renamed, renumbered or moved between tracks without editing a single test. `load_solution` takes one of two things:

- `load_solution(__file__)`, the question's own `solution.py`. This is what every `tests.py` starts with.
- `load_solution("<question name>")`, another question's `solution.py`, by the `name` in its README frontmatter. Names are unique across the whole curriculum (a duplicate raises an error), and are indexed once from the READMEs on disk.

Each loaded solution is keyed by its own path in the module cache, so two questions' identically-named `solution.py` files never collide.

```python
# inside any tests.py
from _load import load_solution

_module = load_solution(__file__)  # this question's own solution
linear = load_solution("linear-regression-hypothesis-function").linear
mse_loss = load_solution("linear-regression-mse-loss").mse_loss
```

`from _load import ...` resolves because `pytest.ini` puts `data/app_data` on the path (`pythonpath = .`), so no test needs a `sys.path` line. The in-browser IDE reads the same two forms: `__file__` is the student's own code, and a name is looked up in the compiled curriculum by question id.

Always run the full suite (`pytest data/app_data/`), not just one question's file in isolation, before trusting a new track — the collision above only ever showed up when tests ran together.

## SQL questions (`tags: [db]`)

Questions tagged `db` (the `03-data-science/04-sql` track) run on real SQLite in the browser (Pyodide's `sqlite3`, version 3.39) instead of the Python harness. The four files keep their names but mean something different:

- **`starter.py`** has two parts split by marker comments. Everything between `-- @schema` and `-- @query` (CREATE/INSERT statements) is loaded into a fresh in-memory database before every Run/Submit and is never shown as editable text; the student sees the `CREATE` statements as comments plus whatever follows `-- @query` (the `-- TODO` task line). Do **not** put the answer in the starter.
- **`solution.py`** is the reference SQL (plain SQL, despite the extension). Only use features SQLite 3.39 has: no `CONCAT()`, and no `date('now')` in anything a test compares (use a fixed date).
- **`tests.py`** is pytest-style, but each test takes a `sql` argument built by `processes/code-execution/sql-runtime.py`: `sql.expect_columns([...])`, `sql.expect_rows([...], ordered=False)`, `sql.rows` / `sql.columns`, `sql.query` (the student's text), `sql.with_data("INSERT ...")` (re-run the student's query on extra hidden rows so a hard-coded answer fails), `sql.plan()` (EXPLAIN QUERY PLAN details), `sql.run(...)`, `sql.table_exists(...)`, `sql.index_columns(...)`. Always include a `with_data` test for result questions.

`pytest` (`npm run test:content`) runs every SQL `tests.py` against its own `solution.py` through `04-sql/conftest.py`, so a broken reference solution is caught in CI. In the browser, Run executes the script and prints the result table or SQLite's own error; Submit runs the tests.

## Libraries beyond NumPy (pandas, matplotlib, seaborn, plotly)

A question's code and tests may import `pandas`, `matplotlib`, `seaborn` or `plotly`. The in-browser runtime loads each library the first time a question that imports it is run (`processes/code-execution/ensure-packages.ts`): pandas and matplotlib come from Pyodide's CDN, and the pure-Python seaborn and plotly wheels are served from this site (`platform/static/wheels/`), so nothing is fetched from PyPI and they are cached by the service worker for offline use. Matplotlib runs on the headless `Agg` backend. Questions that import none of them stay as light as before.

- **Pin versions in two places.** `data/app_data/requirements-test.txt` (and its hash-pinned `.lock`) for CI and the wheels in `platform/static/wheels/` for the browser must name the same versions, so a test sees the same library in both. To change one: download the new wheel from PyPI into that folder, update its entry (file, URL, sha256, size) in `wheels.json` and `BUNDLED_WHEELS` in `ensure-packages.ts`, change `requirements-test.txt`, and regenerate the lock with the command in its header. A unit test checks every file against its recorded checksum.
- **Test the objects, not the pixels.** A chart is built from objects with numbers inside. A matplotlib test reads `ax.lines`, `ax.patches`, `ax.collections` and `ax.get_title()`; a plotly test reads `fig.data` and `fig.layout`. Call `plt.close("all")` at the start of a matplotlib test, and do not call `plt.show()` or `fig.show()`.
- **Do not depend on the order of artists or categories you did not fix.** Seaborn and plotly list categories in order of first appearance and draw hue levels in library-defined order. Pass an explicit `order`/`hue_order`/`category_orders` and compare by name.
- **Check both library generations.** The browser ships older versions than a fresh `pip install` (pandas 2.2 against 3.x, matplotlib 3.8 against 3.11). Run a new question's tests against both before committing; differences show up in return types (`axvspan` returns a `Polygon` in 3.8 and a `Rectangle` later) and in defaults.
- The in-browser test runner supports `pytest.raises` and `pytest.approx` only (see `processes/code-execution/pytest-shim.ts`). Anything else fails with a message naming it.

## `meta.json`: names, topics, company tags

Every root, section and track folder has a `meta.json`. `title` is required and is the name the app shows, so renaming a track is editing one string, and moving it is renaming a folder. Two optional keys are inherited by everything beneath the folder that sets them (the nearest one wins), so a value shared by a whole section is written once, on the section:

```json
{
	"title": "Supervised Models",
	"topics": ["Classical ML"],
	"companies": { "names": ["Netflix", "Spotify"], "roles": "ML Engineer interviews" }
}
```

- `topics`: what the topic filter on the question list matches. Without any, a track falls back to its root's title.
- `companies`: the company-relevance tag shown on a question. Optional; most folders have none.

A section or track folder with only a `meta.json` and no questions yet is a placeholder: it is skipped by the build and appears as soon as it has questions.

## Build

```bash
npm run curriculum:build
```

Walks every root/section/track/question folder under `data/app_data/` and compiles two in-memory outputs, served as Vite virtual modules and never written to disk:

- `virtual:curriculum/bundle`, the IDE bundle (every question's statement, theory, starter, solution and tests).
- `virtual:curriculum/catalogue`, the slim hierarchy `data/questions.ts` adapts for the question list, progress and search pages. It is built from the folders, `meta.json` files, and each README's `name`, `title` and `difficulty` (Beginner/Intermediate/Advanced/Mastery show as Easy/Medium/Hard/Hard), so there is no second list to keep in sync. It is about 40x smaller than the IDE bundle, which is why they are separate files.

`npm run curriculum:build` validates the tree (unique names and titles, every folder has its meta.json) and prints the totals. The dev server runs the same compile on every save, so you only need it to check authoring errors from the command line.
