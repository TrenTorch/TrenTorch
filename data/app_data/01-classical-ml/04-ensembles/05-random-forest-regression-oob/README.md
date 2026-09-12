---
name: ensembles-random-forest-regression-oob
title: 'Random Forest regression, and out-of-bag error estimation'
tags: [classical-ml, ensembles, random-forest, regression]
difficulty: Intermediate
---

## Statement

Implement:

```python
def bootstrap_sample_with_oob(input, targets, seed=None) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Like 02-bagging's bootstrap_sample, plus the indices never drawn."""

def train_random_forest_regressor(input, targets, n_trees, max_depth, seed=None) -> list[tuple[dict, np.ndarray]]:
    """Returns [(tree, oob_indices), ...]."""

def predict_random_forest_regressor(forest, input) -> np.ndarray:
    """Averages every tree's prediction."""

def oob_error(forest, input, targets) -> float:
    """Mean squared error using only each sample's out-of-bag trees."""
```

- Reuse `05-regression-trees`'s `build_regression_tree`/`predict_regression_tree`.
- `predict_random_forest_regressor` averages (regression), it does not vote (`01-random-forest-majority-vote` was for classification).

## Theory

Two small extensions to `02-bagging`, combined into one question because they share the same underlying fact: a bootstrap sample leaves roughly 37% of the original rows out entirely (`02-bagging`'s Theory: about 63% appear, so about 37% don't).

**Regression aggregation** is simpler than classification's vote: average the trees' predictions instead of counting votes. There's no "majority real number," but the mean is the number that minimizes squared error against every tree's opinion, the natural regression analogue.

**Out-of-bag (OOB) error** turns "37% of rows were left out of each tree" from a fact about training into a free validation set. For any given training sample, some trees saw it (it was in their bootstrap sample) and some trees didn't (it was out-of-bag for them). Averaging predictions from _only_ the trees that never saw a sample gives an honest estimate of how the forest performs on unseen data, without holding out a separate validation set at all:

```text
for each training sample i:
    average the predictions of every tree that did NOT include sample i in its bootstrap draw
    compare that average against the true target[i]
```

This is a real, widely-used trick: it means a random forest can report a trustworthy estimate of its own generalization error using only the training set, at essentially no extra cost, since the "held-out" trees already exist as a byproduct of bagging itself.

## Explanation

`bootstrap_sample_with_oob` draws `indices` exactly like `02-bagging`'s `bootstrap_sample`, then builds a boolean `in_bag` array marked `True` at every drawn index, `np.where(~in_bag)[0]` is every index that was never drawn, the out-of-bag set for this specific draw.

`train_random_forest_regressor` follows `02-bagging`'s train loop exactly (one `rng` built once, outside the loop), except each entry collected is a `(tree, oob_indices)` pair, not just the tree, `oob_error` needs to know which samples each tree can honestly be evaluated on.

`predict_random_forest_regressor` is `01-random-forest-majority-vote`'s aggregation with `.mean(axis=0)` in place of a per-sample vote count, the same "stack every tree's predictions, then combine down one axis" shape, a different combination rule for a different kind of target.

`oob_error` accumulates a running `oob_sums`/`oob_counts` per training sample: for each tree, only its own `oob_indices` get predictions added and counted, samples never appearing as anyone's out-of-bag set (`oob_counts == 0`, rare with enough trees, but possible) are excluded from the final average rather than treated as zero-error or crashing the computation.
