---
name: ensembles-regularized-boosting
title: 'Stretch: regularized boosting (shrinkage + L2 leaf penalty, XGBoost-style)'
tags: [classical-ml, ensembles, gradient-boosting, regularization, stretch]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`04-full-boosting-loop` fit every tree greedily: split on whichever feature/threshold reduces variance the most, set each leaf to the mean residual, and repeat. That works, but nothing in it stops a leaf from fitting itself to three noisy points with an extreme value, or a split from looking great only because it isolates a tiny, easily-overfit corner of the data. `06-ridge-regularization` already dealt with an analogous problem for linear weights — add a penalty so an extreme parameter has to earn its size, not just track noise. XGBoost applies the same idea to leaf values in a boosted tree, and derives both a leaf's value and a split's quality directly from the loss function instead of borrowing CART's variance-reduction criterion by convention.

### From theory to code

Theory below derives, from squared-error loss, the closed-form regularized leaf value and the closed-form regularized split gain — both in terms of each sample's gradient and hessian. `xgboost_leaf_value` and `xgboost_split_gain` implement those two formulas directly; `find_best_regularized_split` and `build_regularized_tree` reuse `05-regression-trees`'s tree-building shape with those formulas swapped in for variance reduction and the mean; `train_regularized_boosting`/`predict_regularized_boosting` reuse `04-full-boosting-loop`'s accumulation loop, computing gradients and hessians for squared-error loss each round.

### Constraints

- Squared-error loss throughout: `gradients = predictions - targets` (the derivative of `0.5*(prediction-target)^2` w.r.t. `prediction`), `hessians` are constant `1.0` per sample, every round.
- `xgboost_leaf_value(gradients, hessians, lam)` returns a single `float`: `-sum(gradients) / (sum(hessians) + lam)`.
- `xgboost_split_gain(gradients, hessians, left_mask, lam)` returns a single `float`, using the _parent's_ full gradient/hessian sums together with the left/right sums split by `left_mask`.
- `find_best_regularized_split` returns `None` if no feature has at least 2 distinct values (no valid threshold exists), otherwise `(feature, threshold, gain)` for the best split found, same candidate-threshold search as `05-regression-trees`.
- `build_regularized_tree` recursion stops (returns a leaf) at `max_depth == 0`, fewer than 2 samples, or when `find_best_regularized_split` returns `None` — never split further than that.
- `lam=0` must reduce to (numerically match, within floating-point tolerance) plain unregularized boosting — this is a real sanity check the tests enforce, not a coincidence.
- Reuse `05-regression-trees`'s `predict_regression_tree` for prediction; tree traversal doesn't change, only how leaves and splits are computed at training time.
- `train_regularized_boosting` returns `(initial_prediction, trees)` where `initial_prediction = mean(targets)`; `predict_regularized_boosting` replays `initial_prediction + learning_rate * sum of each tree's prediction`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Both formulas only ever need _sums_ of gradients and hessians — the total, the left-side sum, and the right-side sum. Compute those three pairs once (`G`/`H`, `G_left`/`H_left`, `G_right`/`H_right`) and everything else is arithmetic on scalars.

</details>

<details>
<summary>Hint 2</summary>

`lam` always sits in the denominator, added to a hessian sum, never touching a gradient sum directly. If your leaf value or gain formula adds `lam` anywhere else (to `G`, or outside the fraction), it will pass the `lam=0` case but fail as soon as `lam` actually matters.

</details>

<details>
<summary>Hint 3</summary>

`train_regularized_boosting`'s gradient is `predictions - targets`, not `targets - predictions`. Get the sign backwards and `xgboost_leaf_value`'s `-G/(H+lam)` will push every leaf the wrong direction — the model will get worse every round instead of better.

</details>

## Theory

### The simple version

Imagine grading a leaf's predicted value the way a strict editor grades a claim: a leaf can say something confident, but the more confident it is, the more evidence it needs to back it up. "Evidence" here is how many samples (and how much they agree, via their hessians) land in that leaf. A leaf built from a handful of samples gets pulled back toward a cautious, near-zero value; a leaf built from a lot of consistent evidence is allowed to keep its confident value. `lam` controls how strict the editor is — turn it up and every leaf gets pulled harder toward zero, exactly like `06-ridge-regularization`'s penalty pulled linear weights toward zero.

### The formula

For any twice-differentiable loss, sample `i` contributes a gradient `g_i` (first derivative of the loss w.r.t. the current prediction) and a hessian `h_i` (second derivative). For squared-error loss, `L = 0.5*(prediction - target)^2`:

```text
g_i = prediction_i - target_i
h_i = 1                          (constant: the loss is exactly quadratic)
```

Minimizing the L2-regularized loss within a leaf gives its optimal constant value in closed form:

```text
leaf_value = -G / (H + lam)      where G = sum(gradients), H = sum(hessians)
```

A larger `lam` pulls every leaf's value toward `0` regardless of what the data alone suggests — an explicit ridge penalty on leaf values.

A split's quality follows the same derivation, comparing the best-achievable regularized loss with vs. without the split:

```text
Gain = 0.5 * [ G_left^2/(H_left+lam) + G_right^2/(H_right+lam) - G^2/(H+lam) ]
```

This rewards a split whose children can each be fit with a more extreme (more confident) leaf value than the undivided parent could. `lam` discourages this for small children specifically: a child with few samples has a small `H_left`, so it's penalized more relative to its `G_left` — a built-in defense against splits that only look good because they isolate a handful of samples.

With `lam = 0` and squared-error loss (constant hessians), this reduces to exactly the comparison `05-regression-trees`'s variance reduction makes, just written in gradient/hessian form instead of raw target values — which is why the two produce nearly identical trees at `lam=0`.

### How PyTorch actually implements this

This closed-form gradient/hessian leaf-value and gain derivation is the core idea behind XGBoost (a separate, widely-used gradient-boosting library, not part of PyTorch), and the same gradient-based view of "fit a leaf value that minimizes the loss" is what any second-order or first-order optimizer in `torch.optim` is doing for a differentiable model — computing a gradient (and, for second-order methods, a Hessian or its approximation) and stepping to reduce loss. There is no single PyTorch tensor op that performs this tree-splitting computation, since it's discrete and tree-structured rather than a differentiable operation on a fixed-shape tensor.

## Explanation

`xgboost_leaf_value` and `xgboost_split_gain` are Theory's two formulas translated directly: `np.sum(gradients)` / `np.sum(hessians)` for `G`/`H`, indexed by `left_mask`/`~left_mask` for the two children in the gain formula — `grad_left, hess_left = gradients[left_mask].sum(), hessians[left_mask].sum()` and the mirrored line for the right side.

`find_best_regularized_split` is `05-regression-trees`'s `find_best_regression_split` with `xgboost_split_gain` in place of `variance_reduction`: same feature loop, same `thresholds = (values[:-1] + values[1:]) / 2` midpoint search, different scoring function underneath. `build_regularized_tree` is the same recursive shape as `build_regression_tree`, with `xgboost_leaf_value(gradients, hessians, lam)` for leaves instead of a plain mean, and the same `max_depth == 0 or gradients.size < 2` base case.

`train_regularized_boosting`'s `gradients = predictions - targets` is squared-error loss's actual gradient — not the residual `target - prediction`, the _negative_ of that — matching the sign `xgboost_leaf_value`'s `-G` expects. `hessians = np.ones_like(targets)` is computed once and stays fixed across every round: squared-error loss's second derivative genuinely never changes regardless of the current predictions. Each round builds `tree = build_regularized_tree(input, gradients, hessians, max_depth, lam)`, then updates `predictions = predictions + learning_rate * predict_regression_tree(tree, input)` and appends `tree` — the identical accumulation loop `04-full-boosting-loop` uses. `predict_regularized_boosting` replays the same `initial_prediction + learning_rate * (tree predictions)` sum with no training-time state, which is why it can be called on data the trees never saw.
