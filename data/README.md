# Curriculum Content — Authoring Guide

This is the source of truth for the atomized web curriculum (theory + question + tests + oracle solution, per topic). It is **authored here as real files**, then compiled by `scripts/build-curriculum.mjs` into the JSON the SvelteKit app actually loads at runtime. Never hand-edit generated output — edit the source files here and re-run the build.

This mirrors the pattern the TrenTorch CLI repo already uses: `data/src/<NN>/<NN>.py` (real, authored source) → `tren dev export` → the generated `trentorch` package. Same idea here: author in real `.py`/`.md` files, generate the final bundle as a build artifact.

## Why not one big JSON per question

Test code and oracle solutions are real Python. Stuffing multi-line Python inside a JSON string means no syntax highlighting while writing it, ugly single-line diffs in review, and no way to just run `pytest` on a question to confirm the oracle solution actually passes its own tests before it ever reaches the app. Real `.py` files fix all three. JSON is used only for structured metadata (name, tags, difficulty), which has no reason to be anything else.

## Folder structure

```
data/
  _load.py                       shared, curriculum-wide test-only helper (see below)
  01-<section>/                 e.g. 01-classical-ml, 02-deep-learning, 03-llm, 04-vision-transformer, 05-systems-optimization
    01-<track>/                 e.g. 01-linear-regression, 02-classification
      README.md                 optional: track-level notes
      01-<question-slug>/
        meta.json                name, tags, difficulty
        statement.md             Problem Description — the contract only, never the formula/one-liner answer
        theory.md                the theory, building on the previous question in the track
        starter.py               what the student actually sees first: real signature/docstring, body replaced with TODO + pass
        solution.py              the oracle solution — real, runnable Python
        explanation.md           why the oracle solution is written this specific way
        tests.py                 real pytest file, runnable directly: `pytest tests.py`
      02-<question-slug>/
        ...
```

`starter.py` exists because a student opening a question needs something to actually _do_ — `solution.py` alone is the finished answer with nothing left to implement. `starter.py` keeps the exact same function signature and docstring as `solution.py`, with the body replaced by a short `# TODO` comment (pointing back at Theory, never restating the formula) and a bare `pass`. It is never executed as-is; it exists purely as the starting point handed to a student in the IDE.

Numeric prefixes (`01-`, `02-`, ...) exist at all three levels -- section, track, and question -- purely to fix display/build order. Plain alphabetical folder sort put "classification" before "linear-regression" (wrong pedagogically: Linear Regression teaches the training-loop pattern every later track assumes) and "systems-optimization" before "vision-transformer" (wrong for the same reason, one level up). The prefix is build-order only, not part of the identity: `scripts/build-curriculum.mjs` strips it before exposing `id`/`section`/`track`, so the compiled output and every cross-question reference still use the clean name (`classical-ml`, `linear-regression`), never the numbered folder name. Section and track directory names (after stripping the prefix) are kebab-case and match the `tags` used inside `meta.json`.

## `meta.json` schema

```json
{
	"name": "linear-regression-hypothesis-function",
	"title": "Hypothesis Function",
	"tags": ["classical-ml", "linear-regression", "forward-pass"],
	"difficulty": "Beginner"
}
```

`difficulty` is one of `Beginner`, `Intermediate`, `Advanced`, `Mastery`.

## Reusing an earlier question's solution in a later question's tests

Every question folder's solution file is named `solution.py` — the same name in every folder on purpose (keeps each question self-contained and easy to find). That means they can't all be imported with a plain `import solution` from the same test run without colliding.

**One shared `data/_load.py` for the entire curriculum** (not one per track — an earlier version of this file was duplicated per track, which worked in isolation but collided the moment more than one track's tests ran in the same pytest session: every copy shared the bare module name `_load`, and Python's import cache let whichever track loaded first silently win for every other track too). `load_solution(relative_path)` takes a full path from `data/` and loads that question's `solution.py` under a name unique to that exact path, so two different tracks' `01-...` folders can never collide with each other either:

```python
# inside 01-classical-ml/01-linear-regression/03-mse-gradient/tests.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # data/
from _load import load_solution

linear_forward = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear_forward
mse_loss = load_solution("01-classical-ml/01-linear-regression/02-mse-loss").mse_loss
mse_grad = load_solution("01-classical-ml/01-linear-regression/03-mse-gradient").mse_grad  # this question's own solution, same mechanism
```

Always run the full suite (`pytest data/`), not just one question's file in isolation, before trusting a new track — the collision above only ever showed up when tests ran together.

## Build

```bash
node scripts/build-curriculum.mjs
```

Walks every section/track/question folder and writes the compiled curriculum data the app imports. Run this after adding or editing any question.
