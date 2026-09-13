---
name: classification-softmax-cce
title: 'Stretch: Softmax + Categorical Cross-Entropy'
tags: [classical-ml, classification, multi-class, stretch]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Binary sigmoid chooses between two outcomes. Multiclass classification needs every candidate class to compete for one shared unit of confidence, then needs a loss that scores only the probability assigned to each example's true class.

### From theory to code

Implement row-wise `softmax(Z)` and `cce_loss(P, y_indices)`. Theory maps the stable normalization and the one-correct-class lookup to the exact NumPy operations.

### Constraints

- `Z` and `P` have shape `(n_samples, n_classes)`; each softmax row sums to one.
- `y_indices` has one integer class index per sample.
- Subtract every row's maximum before exponentiating.
- Select one correct-class probability per row, clip it to `[1e-12, 1.0]`, and return a Python `float`.
- Use `P[np.arange(n), y_indices]`, not an all-rows column selection.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Rows are independent probability distributions, so reductions must use `axis=1` and preserve the column dimension.

</details>

<details><summary>Hint 2</summary>

Build row indices with `np.arange(P.shape[0])`; pair them with `y_indices` to gather exactly one value from each row.

</details>

## Theory

### The simple version

Softmax turns a row of competing scores into a budget: raising one class's share lowers the others. Categorical cross-entropy asks only how much of that budget reached the correct class.

### The formula

```text
Z_shift = Z - max(Z, axis=1, keepdims=True)
P = exp(Z_shift) / sum(exp(Z_shift), axis=1, keepdims=True)
p_correct = clip(P[arange(n), y_indices], 1e-12, 1.0)
loss = -mean(log(p_correct))
```

Subtracting the row maximum preserves the probability ratio while preventing a large positive exponent.

### How PyTorch actually implements this

Context only, untested by your submission: `torch.nn.functional.softmax` performs the row normalization and `torch.nn.functional.cross_entropy` is the usual logits-based multiclass loss API.

## Explanation

`Z_shift` uses `axis=1, keepdims=True` so each row's maximum broadcasts across only that row. `exp_Z` is then safe to compute, and the matching row sum normalizes it. In `cce_loss`, `n = P.shape[0]` supplies `np.arange(n)`, making `P[np.arange(n), y_indices]` a paired row/column lookup; clipping and `float(-np.mean(np.log(...)))` finish the scalar loss.
