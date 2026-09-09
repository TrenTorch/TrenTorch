# Curriculum Content — Authoring Guide

This is the source of truth for the atomized web curriculum (theory + question + tests + oracle solution, per topic). It is **authored here as real files**, then compiled by `scripts/build-curriculum.mjs` into the JSON the SvelteKit app actually loads at runtime. Never hand-edit generated output — edit the source files here and re-run the build.

This mirrors the pattern the TrenTorch CLI repo already uses: `data/src/<NN>/<NN>.py` (real, authored source) → `tren dev export` → the generated `trentorch` package. Same idea here: author in real `.py`/`.md` files, generate the final bundle as a build artifact.

## Why not one big JSON per question

Test code and oracle solutions are real Python. Stuffing multi-line Python inside a JSON string means no syntax highlighting while writing it, ugly single-line diffs in review, and no way to just run `pytest` on a question to confirm the oracle solution actually passes its own tests before it ever reaches the app. Real `.py` files fix all three. JSON is used only for structured metadata (name, tags, difficulty), which has no reason to be anything else.

## Folder structure

```
data/
  <section>/                    e.g. classical-ml, deep-learning, llm, vision-transformer, systems-optimization
    <track>/                    e.g. linear-regression
      _load.py                  shared test-only helper (see below)
      README.md                 optional: track-level notes
      01-<question-slug>/
        meta.json                name, tags, difficulty
        statement.md             Problem Description — the contract only, never the formula/one-liner answer
        theory.md                the theory, building on the previous question in the track
        solution.py              the oracle solution — real, runnable Python
        explanation.md           why the oracle solution is written this specific way
        tests.py                 real pytest file, runnable directly: `pytest tests.py`
      02-<question-slug>/
        ...
```

Numeric prefixes (`01-`, `02-`, ...) fix display/dependency order within a track. Section and track directory names are kebab-case and match the `tags` used inside `meta.json`.

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

Every question folder's solution file is named `solution.py` — the same name in every folder on purpose (keeps each question self-contained and easy to find). That means they can't all be imported with a plain `import solution` from the same test run without colliding. `_load.py`, one per track, loads a sibling question's `solution.py` by folder name under a unique internal module name, so a later question's tests can call an earlier question's function without needing it copy-pasted:

```python
# inside 03-mse-gradient/tests.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _load import load_solution

linear_forward = load_solution("01-hypothesis-function").linear_forward
mse_loss = load_solution("02-mse-loss").mse_loss
mse_grad = load_solution("03-mse-gradient").mse_grad
```

## Build

```bash
node scripts/build-curriculum.mjs
```

Walks every section/track/question folder and writes the compiled curriculum data the app imports. Run this after adding or editing any question.
