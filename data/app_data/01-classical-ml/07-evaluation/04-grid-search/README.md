---
name: evaluation-grid-search
title: 'Grid search over a hyperparameter grid'
tags: [classical-ml, evaluation, hyperparameter-tuning]
difficulty: Beginner
---

## Statement

Implement:

```python
def generate_param_combinations(param_grid: dict[str, list]) -> list[dict]: ...
def grid_search(param_grid: dict[str, list], fit_and_score_fn) -> dict: ...
```

- `fit_and_score_fn` is a black box you're given: it trains a model with one specific set of hyperparameters and returns a validation score, higher is better. This question doesn't care what model it is, just how to search over its hyperparameters.

## Theory

Every model built in this curriculum has hyperparameters, `learning_rate`, `max_depth`, `n_trees`, `lam`, chosen by the person training the model, not learned from data the way `weight`/`bias` are. Grid search is the most literal way to pick good ones: define a small set of candidate values for each hyperparameter, try _every combination_ of them, and keep whichever combination scored best on a validation set.

```text
param_grid = {"lr": [0.01, 0.1, 1.0], "depth": [2, 3]}
   ↓ every combination (Cartesian product)
(lr=0.01, depth=2), (lr=0.01, depth=3), (lr=0.1, depth=2), (lr=0.1, depth=3), (lr=1.0, depth=2), (lr=1.0, depth=3)
   ↓ fit_and_score_fn on each
6 scores
   ↓ keep the best
```

The number of combinations multiplies across hyperparameters, `3` learning rates times `2` depths is `6` combinations here, `3` hyperparameters with `5` values each is `125`. This exhaustiveness is grid search's whole appeal (it genuinely checks everything in the grid) and its whole cost (that number grows fast), which is exactly the tradeoff `05-random-search`, the next question in this track, addresses differently.

## Explanation

`generate_param_combinations` uses `itertools.product(*value_lists)`, the standard library's Cartesian product, over the grid's value lists, then `dict(zip(keys, values))` pairs each resulting tuple back up with the original hyperparameter names, turning a tuple like `(0.01, 2)` into `{"lr": 0.01, "depth": 2}`.

`grid_search` calls `fit_and_score_fn` once per combination, tracking the running best (`if score > best_score: ...`) and collecting every `(params, score)` pair into `all_scores` along the way, so the caller can inspect the full grid's results, not just the winner, useful for plotting or sanity-checking that the search actually explored a reasonable range.
