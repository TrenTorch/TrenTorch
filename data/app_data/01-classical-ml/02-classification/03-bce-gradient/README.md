---
name: classification-bce-gradient
title: Gradient of BCE
tags: [classical-ml, classification, manual-calculus, gradients]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`02-bce-loss` says how wrong probability predictions are; training still needs to know how to change the linear parameters that produced them. Once sigmoid and BCE are combined, their derivatives simplify into a residual-like quantity. This question computes its full-batch weight and bias gradients with the column shapes used by the preceding linear-regression exercises.

### From theory to code

Implement `bce_gradient(input, p, target)`. Form the probability error once, then reduce it against features for weights and across samples for bias.

### Constraints

- `input` has shape `(batch_size, in_features)`.
- `p` and `target` both have shape `(batch_size, 1)`.
- Return `grad_weight` with shape `(1, in_features)` and `grad_bias` with shape `(1,)`.
- Average by `n_samples`, not `2 * n_samples`.
- Use matrix multiplication and reductions; do not use autograd or Python loops.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Keep the per-sample discrepancy as a one-column array so it can line up with the feature matrix.

</details>

<details><summary>Hint 2</summary>

Transpose that discrepancy before multiplying by `input`; sum it along axis 0 for the bias.

</details>

## Theory

### The simple version

For logistic regression, the correction signal is simply how much probability was assigned beyond or below the truth. Features that repeatedly accompany that signal need their weights adjusted.

### The formula

```text
error = p - target
grad_weight = (error.T @ input) / n_samples
grad_bias = error.sum(axis=0) / n_samples
```

There is no MSE factor of two: BCE's sigmoid-composed derivative has already simplified to `p - target`.

### How PyTorch actually implements this

Context only, untested by your submission: PyTorch autograd produces these parameter gradients after a binary cross-entropy loss is backpropagated. This exercise requires the manual vectorized form.

## Explanation

`n_samples = input.shape[0]` supplies the mean-gradient denominator. `error = p - target` preserves a `(batch_size, 1)` column. `error.T @ input` therefore returns the required `(1, in_features)` weight gradient, while `error.sum(axis=0)` returns the one-element bias gradient. Both divide by the same `n_samples`, which makes duplicating an entire batch leave its mean gradient unchanged.
