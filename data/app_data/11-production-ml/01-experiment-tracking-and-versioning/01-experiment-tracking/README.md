---
name: production-ml-experiment-tracking
title: 'Experiment Tracking: Logging Hyperparameters, Metrics and Artifacts per Run'
tags: [mlops]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A real ML project runs dozens or hundreds of training attempts, each with slightly different hyperparameters, and each producing metrics that evolve over time and artifacts (checkpoints, plots) worth keeping. Without a structured record of exactly what settings produced exactly what results, "which run was the good one?" becomes an unanswerable question within days. Experiment tracking is the discipline of recording every run's inputs and outputs in one consistent, queryable structure.

### From theory to code

Implement `create_run`, `log_metric`, `log_artifact`, `get_metric_history`, and `get_latest_metric`, the minimal structure of a real experiment-tracking system.

### Constraints

- `create_run(run_id, hyperparameters)` stores a COPY of `hyperparameters` (mutating the caller's dict afterward must not affect the run).
- `log_metric(run, name, value, step)` APPENDS to that metric's history — never overwrites earlier values.
- `log_artifact(run, name, path)` OVERWRITES any earlier artifact registered under the same name.
- `get_latest_metric(run, name)` returns the value at the HIGHEST logged `step`, not necessarily the most recently appended entry.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Metrics and artifacts behave differently on purpose: a metric like "loss" is measured repeatedly over training (you want the whole history), while an artifact like "checkpoint" is a single current reference (you only ever want the latest one).

</details>

<details>
<summary>Hint 2</summary>

`run["metrics"].setdefault(name, []).append((step, value))` handles both "first time logging this metric" and "appending to an existing history" in one line.

</details>

## Theory

### The simple version

Imagine a lab notebook for a scientist running many variations of the same experiment: for each attempt, they write down the exact recipe used (hyperparameters), take repeated measurements as the experiment progresses (metrics, logged at every checkpoint), and file away any physical samples or photographs produced (artifacts) — all clearly labeled with which attempt they belong to. Without this discipline, a scientist who gets a great result on attempt #47 has no way to know, three weeks later, what made attempt #47 different from attempt #46 or #48.

### The formula

```text
create_run(id, hyperparams) = {run_id: id, hyperparameters: copy(hyperparams), metrics: {}, artifacts: {}}

log_metric(run, name, value, step): run.metrics[name].append((step, value))    -- ACCUMULATES
log_artifact(run, name, path): run.artifacts[name] = path                     -- OVERWRITES

get_latest_metric(run, name) = value from the (step, value) pair with the MAX step
```

The asymmetry between `log_metric` (accumulate) and `log_artifact` (overwrite) reflects a real, deliberate design choice in every actual tracking tool: you almost always want a metric's FULL trajectory (to plot a loss curve), but almost never want more than the CURRENT version of a given artifact.

### How PyTorch actually implements this

Context only, untested by your submission: this is the exact API shape of real experiment-tracking tools like MLflow (`mlflow.log_param`, `mlflow.log_metric`, `mlflow.log_artifact`) and Weights & Biases (`wandb.log`) — both distinguish between one-time run metadata (hyperparameters), repeatedly-logged time series (metrics), and file references (artifacts), for exactly the reasons this exercise's structure makes explicit.

## Explanation

`create_run` builds the run record with a defensively-copied hyperparameter dict — `tests.py` confirms mutating the ORIGINAL dict after the run is created has no effect on the stored run, ruling out a version that aliases the caller's dict directly.

`log_metric` appends to a per-metric list, letting the same metric be logged many times across training — `tests.py`'s final oracle test confirms ten successive logs to the same metric name all survive, rather than the tenth silently overwriting the first nine.

`log_artifact` simply overwrites whatever was previously stored under that name, matching the real-world expectation that only the CURRENT checkpoint matters going forward.

`get_metric_history` and `get_latest_metric` provide the two natural ways to consult a metric afterward — the full trajectory, or just the most current (highest-step) reading, which `tests.py` confirms is computed by actual step comparison, not by trusting append order.
