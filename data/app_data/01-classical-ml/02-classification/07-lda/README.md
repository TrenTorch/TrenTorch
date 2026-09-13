---
name: classification-lda
title: Linear Discriminant Analysis (LDA)
tags: [classical-ml, classification, generative-models]
difficulty: Advanced
---

## Statement

### The problem, from first principles

The preceding logistic model learns a boundary directly. LDA instead describes where each class's points tend to lie and how they spread, then derives the boundary from those descriptions. Assuming both classes share one covariance is what makes that boundary linear.

### From theory to code

Implement `lda_fit(X, y)` by splitting classes 0 and 1, estimating their means and shared covariance, then deriving the returned score vector and intercept.

### Constraints

- `X` contains feature rows and `y` contains binary labels `0` and `1`.
- Return `w` with one entry per feature and scalar `b`.
- Pool the two centered scatter matrices and divide by `n - 2`.
- Invert the pooled covariance with `np.linalg.inv`.
- Include the class-prior log ratio in `b`; unequal class sizes must affect the boundary.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Boolean masks `y == 0` and `y == 1` separate the two populations without a loop.

</details>

<details><summary>Hint 2</summary>

Compute each class's centered scatter with `(Xk - muk).T @ (Xk - muk)`, then pool before inverting.

</details>

## Theory

### The simple version

LDA asks which class's shared-shaped cloud better explains a point. Its direction points from the class-0 center toward the class-1 center after accounting for correlated feature spread; its intercept also accounts for which class is more common.

### The formula

```text
S = ((X0-mu0).T @ (X0-mu0) + (X1-mu1).T @ (X1-mu1)) / (n-2)
S_inv = inv(S)
w = S_inv @ (mu1 - mu0)
b = -0.5 * mu1 @ S_inv @ mu1 + 0.5 * mu0 @ S_inv @ mu0 + log((n1/n) / (n0/n))
```

Predict class 1 when `X @ w + b >= 0`.

### How PyTorch actually implements this

Context only, untested by your submission: PyTorch provides the tensor operations used in these estimates, but it has no single core `torch.nn` LDA layer matching this exercise.

## Explanation

`X0, X1` and `mu0, mu1` create the two class estimates. `cov0` and `cov1` are unnormalized centered scatter matrices; `pooled_cov` divides their sum by `n - 2`, spending one degree of freedom on each class mean. `pooled_cov_inv` is reused for both `w` and `b`. Finally, `prior0, prior1` feed the `np.log(prior1 / prior0)` term, shifting the boundary toward a rarer class.
