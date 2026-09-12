---
name: evaluation-random-search
title: 'Random search, contrasted against grid search'
tags: [classical-ml, evaluation, hyperparameter-tuning]
difficulty: Intermediate
---

## Statement

Implement:

```python
def sample_params(param_distributions: dict, rng: np.random.Generator) -> dict: ...
def random_search(param_distributions: dict, n_iter: int, fit_and_score_fn, seed=None) -> dict: ...
```

- Same return shape as `04-grid-search`'s `grid_search`.
- `param_distributions` values are either a `(low, high)` tuple (continuous, sample uniformly in that range) or a list (discrete, sample one value uniformly from it).

## Theory

`04-grid-search` tries _every_ combination in a fixed grid, exhaustive, but the grid itself has to be decided in advance, and its size multiplies across hyperparameters (`03-best-split-minimal-tree`-style combinatorial explosion). Random search takes a different approach entirely: instead of a fixed grid, define a _distribution_ to sample each hyperparameter from, and draw `n_iter` random configurations, trying however many the time budget allows, rather than however many a grid happens to contain.

```text
grid search:    every combination in a FIXED grid, exhaustive but grid-size-bound
random search:  n_iter RANDOM draws from a distribution per hyperparameter, budget-bound
```

The genuinely important, non-obvious advantage: with a continuous hyperparameter (a learning rate, say), grid search only ever tries the exact values you listed, `0.01`, `0.1`, `1.0`, never anything in between, and never anything outside that range. Random search, sampling `uniform(0.001, 1.0)` fresh each time, can land on `0.347` or `0.0623`, values a coarse grid would never test at all. When only one or two hyperparameters actually matter for a given model (a common real finding), random search's freedom to try many different values along the _important_ dimensions, instead of being locked to a grid's fixed handful, tends to find better configurations for the same total number of trials.

## Explanation

`sample_params` checks each hyperparameter's spec: `isinstance(spec, tuple)` means continuous, `rng.uniform(low, high)` draws anywhere in that range, genuinely different values on every call. Otherwise it's a list, `spec[rng.integers(0, len(spec))]` draws one of the fixed discrete choices, uniformly.

`random_search` is structurally `04-grid-search`'s `grid_search` with one difference: instead of iterating over a precomputed list of every combination, it calls `sample_params` fresh, `n_iter` times, with one `rng` built once (outside the loop, the same discipline `02-bagging`/`07-production-mini-batch` rely on) so each iteration draws a genuinely new, independent sample. The rest, tracking the best score and collecting every `(params, score)` pair, is identical to grid search's own bookkeeping.
