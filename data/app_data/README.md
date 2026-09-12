# Curriculum Content — Authoring Guide

This is the source of truth for the atomized web curriculum (theory + question + tests + oracle solution, per topic). It is **authored here as real files**, then compiled by `scripts/build-curriculum.mjs` into the JSON the SvelteKit app actually loads at runtime. Never hand-edit generated output — edit the source files here and re-run the build.

This mirrors the pattern the TrenTorch CLI repo already uses: `data/src/<NN>/<NN>.py` (real, authored source) → `tren dev export` → the generated `trentorch` package. Same idea here: author in real `.py`/`.md` files, generate the final bundle as a build artifact.

## Why not one big JSON per question

Test code and oracle solutions are real Python. Stuffing multi-line Python inside a JSON string means no syntax highlighting while writing it, ugly single-line diffs in review, and no way to just run `pytest` on a question to confirm the oracle solution actually passes its own tests before it ever reaches the app. Real `.py` files fix all three.

## Why one README.md instead of meta.json + statement.md + theory.md + explanation.md

Earlier this content was four separate files per question (`meta.json`, `statement.md`, `theory.md`, `explanation.md`). In practice that meant opening four tabs to read one question end to end, and a metadata-only change (fixing a tag) sat in its own file next to prose it had nothing to do with. A single `README.md` — frontmatter for the structured fields, then the three markdown sections in reading order — is both the file a human opens first when browsing the folder in GitHub and the one file `scripts/build-curriculum.mjs` needs to parse for everything but the code. `starter.py`, `solution.py` and `tests.py` stay separate real `.py` files (the reasoning above still applies to those).

## Folder structure

```
data/
  app_data/                      compiled curriculum content (this folder)
    _load.py                     shared, curriculum-wide test-only helper (see below)
    01-<section>/                e.g. 01-classical-ml, 02-deep-learning, 03-llm, 04-vision-transformer, 05-systems-optimization
      01-<track>/                e.g. 01-linear-regression, 02-classification
        01-<question-slug>/
          README.md              frontmatter (name, tags, difficulty) + ## Statement / ## Theory / ## Explanation
          starter.py              what the student actually sees first: real signature/docstring, body replaced with TODO + pass
          solution.py             the oracle solution — real, runnable Python
          tests.py                real pytest file, runnable directly: `pytest tests.py`
        02-<question-slug>/
          ...
  user_data/                     schema for what the app persists client-side — see data/user_data/README.md
```

`starter.py` exists because a student opening a question needs something to actually _do_ — `solution.py` alone is the finished answer with nothing left to implement. `starter.py` keeps the exact same function signature and docstring as `solution.py`, with the body replaced by a short `# TODO` comment (pointing back at Theory, never restating the formula) and a bare `pass`. It is never executed as-is; it exists purely as the starting point handed to a student in the IDE.

Numeric prefixes (`01-`, `02-`, ...) exist at all three levels -- section, track, and question -- purely to fix display/build order. Plain alphabetical folder sort put "classification" before "linear-regression" (wrong pedagogically: Linear Regression teaches the training-loop pattern every later track assumes) and "systems-optimization" before "vision-transformer" (wrong for the same reason, one level up). The prefix is build-order only, not part of the identity: `scripts/build-curriculum.mjs` strips it before exposing `id`/`section`/`track`, so the compiled output and every cross-question reference still use the clean name (`classical-ml`, `linear-regression`), never the numbered folder name. Section and track directory names (after stripping the prefix) are kebab-case and match the `tags` used inside each question's `README.md` frontmatter.

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

The frontmatter block is a small fixed subset of YAML (plain scalars plus one `[a, b, c]` flow sequence for `tags`) parsed by hand in `scripts/build-curriculum.mjs` — not a general YAML parser, so keep values plain. `difficulty` is one of `Beginner`, `Intermediate`, `Advanced`, `Mastery`. The three `##` sections must appear in exactly that order (Statement, then Theory, then Explanation) — the build fails loudly if one is missing or out of order, rather than silently shipping a blank tab in the IDE.

## Reusing an earlier question's solution in a later question's tests

Every question folder's solution file is named `solution.py` — the same name in every folder on purpose (keeps each question self-contained and easy to find). That means they can't all be imported with a plain `import solution` from the same test run without colliding.

**One shared `data/app_data/_load.py` for the entire curriculum** (not one per track — an earlier version of this file was duplicated per track, which worked in isolation but collided the moment more than one track's tests ran in the same pytest session: every copy shared the bare module name `_load`, and Python's import cache let whichever track loaded first silently win for every other track too). `load_solution(relative_path)` takes a full path from `data/app_data/` and loads that question's `solution.py` under a name unique to that exact path, so two different tracks' `01-...` folders can never collide with each other either:

```python
# inside 01-classical-ml/01-linear-regression/03-mse-gradient/tests.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # data/app_data/
from _load import load_solution

linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear
mse_loss = load_solution("01-classical-ml/01-linear-regression/02-mse-loss").mse_loss
mse_gradient = load_solution("01-classical-ml/01-linear-regression/03-mse-gradient").mse_gradient  # this question's own solution, same mechanism
```

Always run the full suite (`pytest data/app_data/`), not just one question's file in isolation, before trusting a new track — the collision above only ever showed up when tests ran together.

## Build

```bash
node scripts/build-curriculum.mjs
```

Walks every section/track/question folder under `data/app_data/` and writes the compiled curriculum data the app imports. Run this after adding or editing any question.
