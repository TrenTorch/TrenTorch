# Curriculum Content — Authoring Guide

This is the source of truth for the atomized web curriculum (theory + question + tests + oracle solution, per topic). It is **authored here as real files**, then compiled by `processes/curriculum-build/build.mjs` into the JSON the SvelteKit app actually loads at runtime. Never hand-edit generated output — edit the source files here and re-run the build.

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

Walks every root/section/track/question folder under `data/app_data/` and writes two files into `data/curriculum/`, both generated, never hand-edited:

- `generated-curriculum.json`, the IDE bundle (every question's statement, theory, starter, solution and tests).
- `generated-catalogue.json`, the slim hierarchy `data/questions.ts` adapts for the question list, progress and search pages. It is built from the folders, `meta.json` files, and each README's `name`, `title` and `difficulty` (Beginner/Intermediate/Advanced/Mastery show as Easy/Medium/Hard/Hard), so there is no second list to keep in sync. It is about 40x smaller than the IDE bundle, which is why they are separate files.

Run this after adding, moving or editing any question. `npm run curriculum:check` fails if the committed files are stale.
