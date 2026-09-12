---
name: ensembles-regularized-boosting
title: 'Stretch: regularized boosting (shrinkage + L2 leaf penalty, XGBoost-style)'
tags: [classical-ml, ensembles, gradient-boosting, regularization, stretch]
difficulty: Advanced
---

## Statement

Implement:

```python
def xgboost_leaf_value(gradients, hessians, lam) -> float: ...
def xgboost_split_gain(gradients, hessians, left_mask, lam) -> float: ...
def find_best_regularized_split(input, gradients, hessians, lam) -> tuple[int, float, float] | None: ...
def build_regularized_tree(input, gradients, hessians, max_depth, lam) -> dict: ...
def train_regularized_boosting(input, targets, n_trees, max_depth, learning_rate, lam) -> tuple[float, list[dict]]: ...
def predict_regularized_boosting(initial_prediction, trees, learning_rate, input) -> np.ndarray: ...
```

- Reuse `05-regression-trees`'s `predict_regression_tree` for prediction, tree traversal doesn't change.
- Squared-error loss throughout, so hessians are constant (`1.0` per sample).
- `lam=0` should behave almost identically to `04-full-boosting-loop`'s plain gradient boosting, this is a real sanity check, not a coincidence.

## Theory

`04-full-boosting-loop` fit each tree greedily, splitting on variance reduction and setting each leaf to the mean residual, with no explicit control over how extreme a leaf's value could get. XGBoost's contribution (among others) is deriving what a leaf's value and a split's quality _should_ be from the loss function directly, with an explicit L2 penalty on leaf values baked into the derivation, rather than reusing CART's variance-reduction criterion by convention.

For any twice-differentiable loss, each sample contributes a gradient `g_i` (first derivative of the loss w.r.t. the current prediction) and a hessian `h_i` (second derivative). For squared-error loss, `L = 0.5*(prediction - target)^2`, these are simple: `g_i = prediction_i - target_i`, `h_i = 1` for every sample, the loss is exactly quadratic, so its second derivative never changes.

Minimizing the (L2-regularized) loss within a leaf gives its optimal constant value in closed form:

```text
leaf_value = -G / (H + lam)      where G = sum(gradients), H = sum(hessians)
```

`lam` (the L2 penalty strength) sits in the denominator: a larger `lam` pulls every leaf's value toward `0`, regardless of what the data alone would suggest, exactly a ridge penalty (`06-ridge-regularization`, one track over) applied to leaf values instead of linear weights.

A split's quality follows from the same derivation, comparing the best-achievable regularized loss with vs. without the split:

```text
Gain = 0.5 * [ G_left^2/(H_left+lam) + G_right^2/(H_right+lam) - G^2/(H+lam) ]
```

which rewards a split whose children can each be fit with a more extreme (more confident) leaf value than the undivided parent could, `lam` discourages this for small children (a child with few samples, small `H_left`, gets penalized more relative to its `G_left`), a built-in defense against splits that only look good because they isolate a handful of samples.

With `lam = 0` and squared-error loss (constant hessians), this reduces to the exact same comparison `05-regression-trees`'s variance reduction makes, just written in gradient/hessian form instead of raw target values, which is why the two produce nearly identical trees at `lam=0`.

## Explanation

`xgboost_leaf_value` and `xgboost_split_gain` are the two formulas above, translated directly: `np.sum(gradients)` / `np.sum(hessians)` for `G`/`H`, indexed by `left_mask`/`~left_mask` for the two children in the gain formula.

`find_best_regularized_split` is `05-regression-trees`'s `find_best_regression_split` with `xgboost_split_gain` in place of `variance_reduction`, same feature/threshold search, different scoring function underneath. `build_regularized_tree` is the same recursive shape as `build_regression_tree`, with `xgboost_leaf_value` for leaves instead of a plain mean.

`train_regularized_boosting`'s `gradients = predictions - targets` is squared-error loss's actual gradient (not the residual `target - prediction`, the _negative_ of that, this is the loss's own derivative, matching the sign the leaf-value formula's `-G` expects), and `hessians = np.ones_like(targets)` stays fixed for every round, squared-error loss's second derivative genuinely never changes regardless of the current predictions. Everything else, the accumulation loop and `predict_regularized_boosting`, is identical in shape to `04-full-boosting-loop`.
