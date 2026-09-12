---
name: decision-trees-regression-trees
title: 'Regression trees: splitting on variance reduction instead of Gini'
tags: [classical-ml, decision-trees, regression]
difficulty: Intermediate
---

## Statement

Implement, mirroring `01-gini-impurity` through `03-best-split-minimal-tree` for continuous targets instead of class labels:

```python
def variance(targets: np.ndarray) -> float: ...
def variance_reduction(parent_targets, left_targets, right_targets) -> float: ...
def find_best_regression_split(input, targets) -> tuple[int, float, float] | None: ...
def build_regression_tree(input, targets, max_depth) -> dict: ...
def predict_regression_tree(tree, input) -> np.ndarray: ...
```

- `targets` are real-valued, not class labels, `np.array([2.3, -1.0, 4.7])` is a completely ordinary input.
- A leaf's prediction is the _mean_ of its node's targets, not a majority vote, there's no "most common" real number.
- `predict_regression_tree` returns a float array, `predict_tree` (from `03-best-split-minimal-tree`) returns integer class labels, don't reuse it here, its output dtype would silently truncate real-valued predictions.

## Theory

Everything about tree-building so far assumed the target is a class label, "which of these discrete categories," and Gini impurity measured how mixed those categories were. Regression asks a different question, "predict a number," so a node's quality needs a different measure entirely: **variance**. A node where every target is close to the same value has low variance and is easy to predict well with a single number, its own mean. A node with wildly scattered targets has high variance, no single number predicts it well.

```text
variance(targets) = mean((targets - mean(targets))^2)
```

Every other piece carries over structurally unchanged. `information_gain` became `variance_reduction`, same size-weighted before-vs-after comparison, just measuring impurity with variance instead of Gini:

```text
Reduction = Var(parent) - [ (n_left/n) * Var(left) + (n_right/n) * Var(right) ]
```

`find_best_split` became `find_best_regression_split`, identical search over every feature and every candidate threshold, just scored by `variance_reduction` instead of `information_gain`. `build_tree` became `build_regression_tree`, identical recursive structure and stopping conditions, a "pure" regression node is one where every target is already identical (`variance == 0`) rather than every label being identical. The only place the two genuinely diverge is the leaf's prediction: a classification leaf votes for the majority class, a regression leaf predicts the mean, the single number that minimizes squared error against everything in that leaf.

`scikit-learn`'s `DecisionTreeRegressor(criterion='squared_error')` is this exact algorithm.

## Explanation

`variance(targets)` is `np.var(targets)` guarded for the empty case the same way `01-gini-impurity` guards `labels.size == 0`, an empty node has nothing to be variable about.

`variance_reduction` and `find_best_regression_split` are `02-information-gain` and `03-best-split-minimal-tree`'s `find_best_split` with every `gini_impurity`/`information_gain` call swapped for `variance`/`variance_reduction`, the weighting-by-child-size logic is identical, only the impurity measure underneath changed.

`build_regression_tree`'s leaf case is `{"leaf": True, "prediction": float(np.mean(targets))}`, `float(...)` because `np.mean` returns a NumPy scalar, matching the same discipline `02-mse-loss` uses for its own scalar returns.

`predict_regression_tree` walks the tree exactly like `predict_tree` does, the only difference is `np.empty(input.shape[0], dtype=float)` instead of `dtype=int`, since these predictions are real numbers, not class indices.
