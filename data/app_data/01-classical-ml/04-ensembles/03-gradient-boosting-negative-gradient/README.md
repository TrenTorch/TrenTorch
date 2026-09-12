---
name: ensembles-gradient-boosting-negative-gradient
title: 'Gradient Boosting: fit one tree to the negative gradient of the loss'
tags: [classical-ml, ensembles, gradient-boosting]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Bagging trains independent trees. Boosting trains the next tree specifically to correct the current ensemble's remaining errors. For squared error, that correction target has a simple exact form: the signed residual.

### From theory to code

Implement `negative_gradient` and `fit_tree_to_negative_gradient`, using the existing regression-tree builder to fit the current residuals rather than original targets.

### Constraints

- `targets` and `predictions` have matching shapes.
- The negative gradient is `targets - predictions`, not the opposite sign.
- A perfect prediction produces a zero gradient.
- Fit `build_regression_tree(input, residuals, max_depth)`.
- Do not rebuild regression-tree logic here.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

For a squared-error underprediction, the correction must be positive.

</details>

<details><summary>Hint 2</summary>

Compute the residual through `negative_gradient`, then pass it as the tree's target array.

</details>

## Theory

### The simple version

The current model leaves some examples too high and some too low. A boosting tree learns a map of those signed leftovers, so adding its output pushes each prediction in the loss-reducing direction.

### The formula

```text
L = 0.5 * (target - prediction) ** 2
-dL/dprediction = target - prediction
residuals = negative_gradient(targets, predictions)
tree = build_regression_tree(input, residuals, max_depth)
```

### How PyTorch actually implements this

Context only, untested by your submission: boosting is usually implemented by tree libraries; PyTorch autograd can provide gradients for differentiable models, but this exercise explicitly fits a tree to the squared-error negative gradient.

## Explanation

`negative_gradient` returns `targets - predictions` directly, preserving both shape and sign. `fit_tree_to_negative_gradient` names that value `residuals`, then passes it to `build_regression_tree`. With zero current predictions, residuals equal targets; with already-good predictions, the tree learns only the remaining small errors.
