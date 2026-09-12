---
name: ensembles-full-boosting-loop
title: 'Full boosting loop: assemble a minimal booster'
tags: [classical-ml, ensembles, gradient-boosting]
difficulty: Advanced
---

## Statement

Implement:

```python
def train_gradient_boosting(input, targets, n_trees, max_depth, learning_rate) -> tuple[float, list[dict]]:
    """Returns (initial_prediction, trees)."""

def predict_gradient_boosting(initial_prediction, trees, learning_rate, input) -> np.ndarray:
    """Replays training's accumulation on new data."""
```

- Reuse `03-gradient-boosting-negative-gradient`'s `fit_tree_to_negative_gradient` and `05-regression-trees`'s `predict_regression_tree`, don't reimplement either.
- `learning_rate` scales every tree's contribution, applied identically during training and prediction.

## Theory

`03-gradient-boosting-negative-gradient` built one round: fit a tree to the current residual. A full booster repeats that round `n_trees` times, each round's tree correcting whatever every _previous_ round still got wrong, and adds every tree's (scaled) prediction together to form the final one.

```text
prediction_0 = mean(targets)                          # the simplest possible constant model
for each round:
    residual = targets - prediction                    # 03's negative_gradient
    tree = fit a regression tree to residual            # 03's fit_tree_to_negative_gradient
    prediction = prediction + learning_rate * tree(input)
```

`learning_rate` (sometimes called shrinkage) scales down each tree's contribution, `0.1` is a common real-world default. Without it, the very first tree could already fit the training residuals almost perfectly, leaving nothing meaningful for later trees to correct and overfitting hard to the first tree's specific mistakes. With it, each tree takes a smaller step, and many small, cautious steps generalize better than one large, confident one, the same bias-variance intuition behind a small learning rate in gradient descent itself (`04-gd-step`'s Theory, one level up: too large a step overshoots and destabilizes, too small is slow but steadier).

`predict_gradient_boosting` exists as a separate function from training because a real model needs to predict on data it never trained on, replaying the _same_ accumulation (`initial_prediction`, then every tree's contribution in the same order, scaled by the same `learning_rate`) on a new `input` array is the actual definition of "using a trained gradient boosting model," not just an implementation convenience.

## Explanation

`train_gradient_boosting`'s `initial_prediction = float(np.mean(targets))` is the simplest model with no features at all, the constant that minimizes squared error before any tree exists. `predictions = np.full(targets.shape[0], initial_prediction)` starts every sample at that same constant.

Each loop iteration calls `fit_tree_to_negative_gradient(input, targets, predictions, max_depth)` against the _current_ `predictions`, not the original constant, `predictions` is updated in place across iterations specifically so each new tree sees what all previous trees have already corrected. `predictions = predictions + learning_rate * predict_regression_tree(tree, input)` is the accumulation step, and the same tree object is appended to `trees` so `predict_gradient_boosting` can replay this exact process later.

`predict_gradient_boosting` is deliberately the same accumulation logic with `input` swapped for new data, `np.full(input.shape[0], initial_prediction)` followed by a loop adding `learning_rate * predict_regression_tree(tree, input)` for every tree in the same order they were trained.
