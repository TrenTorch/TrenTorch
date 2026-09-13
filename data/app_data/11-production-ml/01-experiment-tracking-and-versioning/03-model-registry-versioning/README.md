---
name: production-ml-model-registry-versioning
title: 'Model Versioning and a Model Registry: Promoting a Run to a Named, Deployable Version'
tags: [mlops]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`01-experiment-tracking` produces many runs, each with its own metrics — but a run isn't automatically "the model in production." A model registry is the missing piece between experimentation and deployment: a named, versioned record that tracks WHICH run became WHICH numbered version of a model, and WHICH version (if any) is currently promoted to serve real traffic.

### From theory to code

Implement `create_registry`, `register_model_version` (linking a run to a new, sequentially-numbered model version), `promote_to_stage` (moving a version between lifecycle stages), and `get_version_at_stage`.

### Constraints

- `register_model_version(registry, model_name, run_id, metrics)` assigns sequential version numbers PER model name, starting at `1`; new versions start in stage `"none"`.
- `promote_to_stage(registry, model_name, version, stage)` raises `ValueError` for an unrecognized stage.
- Promoting a version to `"production"` must automatically move whatever OTHER version was previously `"production"` to `"archived"` — at most one version can be `"production"` at a time.
- `get_version_at_stage(registry, model_name, stage)` returns the matching version dict, or `None` if none match.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Version numbers are `len(existing_versions) + 1` — a simple, deterministic counter scoped to each model name independently, so two different models both start numbering from `1`.

</details>

<details>
<summary>Hint 2</summary>

`promote_to_stage`'s "at most one production version" rule needs a loop over ALL of a model's versions: set the TARGET version to the new stage, and separately check every OTHER version — if it's currently `"production"` and the new stage being applied is `"production"`, demote it to `"archived"`.

</details>

## Theory

### The simple version

Imagine a company's official product catalog, where every prototype gets a sequential model number as it's built, and at any given time exactly ONE numbered prototype is marked "currently shipping" — when a new prototype is approved for shipping, the OLD shipping prototype automatically gets relabeled "retired," never left ambiguously co-shipping alongside the new one. A model registry enforces exactly this discipline for ML models: it's the single source of truth for "which version is actually live right now," which is essential the moment more than one person or system needs to agree on that answer.

### The formula

```text
register_model_version(registry, name, run_id, metrics):
    version_number = len(registry[name]) + 1
    registry[name].append({version, run_id, metrics, stage: "none"})

promote_to_stage(registry, name, version, stage):
    for entry in registry[name]:
        if entry.version == version: entry.stage = stage
        elif stage == "production" and entry.stage == "production": entry.stage = "archived"

get_version_at_stage(registry, name, stage) = first entry with entry.stage == stage, or None
```

The automatic-archiving rule when promoting to `"production"` isn't an incidental implementation detail — it's the entire reason a model registry is trustworthy: any downstream system that queries "what's currently in production" gets a well-defined, unambiguous single answer, by construction, never a race between two versions both claiming that title.

### How PyTorch actually implements this

Context only, untested by your submission: this is the exact concept behind MLflow's Model Registry (`mlflow.register_model`, `client.transition_model_version_stage`), which uses the identical stage vocabulary (`None`, `Staging`, `Production`, `Archived`) and the same "promoting to Production auto-archives the previous Production version" behavior this exercise reimplements from scratch.

## Explanation

`register_model_version` computes each new version's number from the current length of that model's version list, appending a fresh entry that starts unpromoted — `tests.py` confirms two different model names get independently numbered version sequences.

`promote_to_stage` walks every version of the named model, applying the requested stage change to the target version while enforcing the "single production version" invariant on every OTHER version — `tests.py`'s final oracle test runs FIVE successive promotions to production and confirms, after each one, that EXACTLY one version is ever marked production, directly ruling out a mutant that forgets to demote the previous holder.

`get_version_at_stage` is a straightforward linear search — `tests.py` confirms it returns `None` cleanly when no version currently occupies the requested stage, rather than raising or returning something misleading.
