---
name: ensembles-newton-leaf-weights
title: 'Newton leaf weights and split gain'
tags: [classical-ml, supervised, ensembles, gradient-boosting, second-order]
difficulty: Advanced
---

## Statement

### Second-order boosting for logistic loss

Modern gradient boosting uses both the gradient g and the Hessian h of the loss at each point. For logistic loss with raw score f, the gradient is p − y and the Hessian is p(1 − p), where p = sigmoid(f).

Implement three functions.

**`logistic_grad_hess(y, raw)`** returns `(g, h)` for labels `y` in `{0, 1}` and raw scores `raw`.

**`leaf_weight(G, H, lam)`** returns the optimal leaf value −G / (H + λ).

**`split_gain(G_L, H_L, G_R, H_R, lam, gamma)`** returns ½ · (G_L²/(H_L + λ) + G_R²/(H_R + λ) − G²/(H + λ)) − γ, where G = G_L + G_R and H = H_L + H_R.

### Constraints

- `lam` must be positive, otherwise raise `ValueError` in `leaf_weight` and `split_gain`.
- `y` values must be 0 or 1, otherwise raise `ValueError` in `logistic_grad_hess`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

For the sigmoid, `1 / (1 + np.exp(-raw))` is enough for the test values.

</details>

## Theory

A second-order step is the minimizer of the quadratic approximation of the loss in the leaf. Dividing by H + λ shrinks leaves with little curvature, and λ is the regularization that keeps the step bounded.

## Explanation

The gradient and Hessian come from the sigmoid. The leaf weight and split gain are closed forms in the sums of g and h, so a tree builder only needs to accumulate those sums per node.
