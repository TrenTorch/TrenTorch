---
name: support-vector-machines-polynomial-kernel
title: Polynomial kernel
tags: [classic-ml]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`Linear kernel` gives straight boundaries, and `RBF kernel` gives bumpy ones driven by distance. A polynomial kernel sits between them: it raises a shifted, scaled dot product to a power, so the boundary can bend in controlled, polynomial ways. Degree `1` is the linear kernel again, and higher degrees allow more curvature.

Given `X` with shape `(n, d)` and `Y` with shape `(m, d)`, return the `(n, m)` matrix of polynomial similarities.

### Constraints

- Return an array of shape `(n, m)` where entry `[i, j]` equals `(gamma * X[i] @ Y[j] + coef0) ** degree`.
- Defaults: `degree=3`, `coef0=1.0`, `gamma=1.0`.
- Build it on top of `linear_kernel` from the previous question, which is already available to load.
- Do not modify `X` or `Y`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Call `linear_kernel(X, Y)` for the dot products, then scale, shift, and raise to a power, all elementwise.

</details>

<details>
<summary>Hint 2</summary>

Scale before you shift: `gamma * dots + coef0`, not `gamma * (dots + coef0)`.

</details>

## Theory

### The simple version

Take the dot product, which measures alignment, multiply it by a scale, add a constant, and then raise the whole thing to a power. Each extra degree lets the decision boundary bend one more time. The constant `coef0` controls how much the lower-order terms count against the higher ones.

### The formula

$$
k_{\text{poly}}(x, y) = \left(\gamma\, x^\top y + c\right)^{d}
$$

where $c$ is `coef0` and $d$ is `degree`. With $c = 0$ and $d = 1$ this reduces to the linear kernel when $\gamma = 1$.

## Explanation

`polynomial_kernel` loads `linear_kernel` from its own question and applies the formula from Theory elementwise to its output. Scaling by `gamma` and adding `coef0` happen before the power, which is what the formula says.
