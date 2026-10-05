---
name: evaluation-random-search
title: 'Random search, contrasted against grid search'
tags: [classical-ml, evaluation, hyperparameter-tuning]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`04-grid-search` tries every combination in a fixed grid — exhaustive, but the grid itself has to be decided in advance, and its size multiplies across hyperparameters the same way a decision tree's split search grows combinatorially (`03-best-split-minimal-tree`). A learning rate grid of `[0.01, 0.1, 1.0]` will never test `0.347`, no matter how good that value might be, because it was never in the list.

The fix doesn't need a smarter search order, just a different way of generating candidates: instead of a fixed, pre-listed grid, define a _distribution_ to draw each hyperparameter from, and sample as many random configurations as the time budget allows, rather than however many a grid happens to contain.

### From theory to code

Implement `sample_params(param_distributions, rng)` to draw one random configuration, then `random_search(param_distributions, n_iter, fit_and_score_fn, seed=None)` to repeat that `n_iter` times and track the best, mirroring `04-grid-search`'s `grid_search` bookkeeping.

### Constraints

- `param_distributions` values are either a `(low, high)` tuple (continuous — sample uniformly in that range) or a list (discrete — sample one value uniformly from it).
- `sample_params` returns one dict of hyperparameter values, one draw per key in `param_distributions`.
- `random_search` returns the same shape as `04-grid-search`'s `grid_search`: `{"best_params", "best_score", "all_scores"}`, with `all_scores` holding exactly `n_iter` `(params, score)` pairs.
- Build exactly one `np.random.default_rng(seed)` before the sampling loop — not one per iteration.
- The same `seed` must reproduce identical `all_scores` and `best_params` across calls.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`sample_params` just needs to tell continuous from discrete specs apart: `isinstance(spec, tuple)` is the continuous case, anything else (a list) is discrete.

</details>

<details>
<summary>Hint 2</summary>

For continuous, `rng.uniform(low, high)` draws anywhere in the range. For discrete, don't reach for `rng.choice` — index the list with a random integer, `spec[rng.integers(0, len(spec))]`.

</details>

<details>
<summary>Hint 3</summary>

`random_search` is structurally identical to `grid_search`, with one swap: instead of iterating a precomputed list of combinations, call `sample_params` fresh inside the loop, `n_iter` times, using the _same_ `rng` object each time so the draws are independent, not repeated.

</details>

## Theory

### The simple version

Grid search only ever tastes the exact ingredients on its shopping list. Random search shops freely within a budget instead — draw `n_iter` random configurations from a distribution over each hyperparameter, and however many the time budget allows is exactly how many get tried, with no grid to be locked into.

```text
grid search:    every combination in a FIXED grid, exhaustive but grid-size-bound
random search:  n_iter RANDOM draws from a distribution per hyperparameter, budget-bound
```

The genuinely important, non-obvious advantage: with a continuous hyperparameter, grid search only ever tries the exact values listed — `0.01`, `0.1`, `1.0` — never anything in between or outside that range. Random search, sampling `uniform(0.001, 1.0)` fresh each time, can land on `0.347` or `0.0623`, values a coarse grid would never test at all. When only one or two hyperparameters actually matter for a given model (a common real finding), random search's freedom to try many different values along the _important_ dimensions, instead of being locked to a grid's fixed handful, tends to find better configurations for the same total number of trials.

### The formula

```text
sample_params(param_distributions, rng):
    for key, spec in param_distributions.items():
        if spec is a (low, high) tuple: params[key] = rng.uniform(low, high)
        else (spec is a list):          params[key] = spec[rng.integers(0, len(spec))]

random_search:
    rng = default_rng(seed)          # built once
    repeat n_iter times:
        params = sample_params(param_distributions, rng)
        score  = fit_and_score_fn(params)
        track best_params/best_score, append (params, score) to all_scores
```

### How PyTorch actually implements this

Context only, untested by your submission: like grid search, this is a search-loop utility around training, not a `torch.nn` layer. `sklearn.model_selection.RandomizedSearchCV` and libraries like Optuna implement the same sample-and-score idea, typically layering a smarter proposal strategy on top of pure random draws (see `06-bayesian-optimization`).

## Explanation

`sample_params` checks each hyperparameter's spec: `isinstance(spec, tuple)` means continuous, and `rng.uniform(low, high)` draws anywhere in that range, genuinely different values on every call — `test_sample_params_continuous_produces_varied_values_not_grid_points` checks for exactly this, more than 15 distinct rounded values out of 20 draws. Otherwise it's a list, and `spec[rng.integers(0, len(spec))]` draws one of the fixed discrete choices, uniformly.

`random_search` is structurally `04-grid-search`'s `grid_search` with one difference: instead of iterating over a precomputed list of every combination, it calls `sample_params` fresh, `n_iter` times, with one `rng = np.random.default_rng(seed)` built once outside the loop — the same discipline `02-bagging`/`07-production-mini-batch` rely on — so each iteration draws a genuinely new, independent sample rather than repeating the same "random" value. `test_rng_is_built_once_not_reseeded_every_iteration` targets exactly the mutant that would reseed inside the loop: with a fixed seed, every draw would then collapse to the same number. The rest — tracking the best score with `if score > best_score`, and collecting every `(params, score)` pair into `all_scores` — is identical to grid search's own bookkeeping.
