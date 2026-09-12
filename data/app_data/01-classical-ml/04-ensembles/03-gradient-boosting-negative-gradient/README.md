---
name: ensembles-gradient-boosting-negative-gradient
title: 'Gradient Boosting: fit one tree to the negative gradient of the loss'
tags: [classical-ml, ensembles, gradient-boosting]
difficulty: Intermediate
---

## Statement

Implement:

```python
def negative_gradient(targets: np.ndarray, predictions: np.ndarray) -> np.ndarray: ...

def fit_tree_to_negative_gradient(
    input: np.ndarray, targets: np.ndarray, predictions: np.ndarray, max_depth: int
) -> dict: ...
```

- Reuse `05-regression-trees`'s `build_regression_tree`, don't reimplement it.
- This uses squared-error loss throughout: `L = 0.5 * (target - prediction)^2`.

## Theory

Random Forest (`01-random-forest-majority-vote`, `02-bagging`) trains many trees _independently_, in parallel, on different resampled data, then averages their opinions. Gradient boosting trains trees _sequentially_, each new tree looking specifically at what the ensemble so far got wrong, and gets added to correct it.

"What the ensemble got wrong" is made precise by the loss function's gradient. For squared-error loss, `L = 0.5 * (target - prediction)^2`, the gradient with respect to the prediction is `dL/d(prediction) = prediction - target`. The **negative** gradient, `target - prediction`, points in the direction that reduces loss, and for squared error it's exactly the residual, how far off the current prediction is, and in which direction.

```text
current ensemble predictions
        ↓
negative_gradient = target - prediction   (the residual, for squared error)
        ↓
fit a new regression tree to PREDICT that residual
        ↓
add (a scaled copy of) that tree's predictions to the ensemble
```

This is the same "gradient" idea `03-mse-gradient` used for a single linear model's parameters, generalized: instead of asking "how should I nudge a _number_ (a weight) to reduce loss," gradient boosting asks "how should I nudge the _function_ (the ensemble's prediction) to reduce loss," and answers it by fitting a tree that approximates exactly that nudge. `04-full-boosting-loop`, the next question in this track, repeats this step many times, each new tree correcting what all the previous ones still got wrong.

## Explanation

`negative_gradient(targets, predictions)` is `targets - predictions`, the residual, this is literally what "negative gradient of squared-error loss" evaluates to, not merely a convenient approximation of it.

`fit_tree_to_negative_gradient` computes those residuals first, then calls `build_regression_tree(input, residuals, max_depth)`, the tree's job is predicting _how wrong the ensemble currently is at each point_, not predicting `targets` directly, that distinction is the entire mechanism of boosting.
