---
name: support-vector-machines-rbf-kernel
title: RBF kernel
tags: [classic-ml]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`Linear kernel` measures similarity with a dot product, which only ever draws straight boundaries. The radial basis function (RBF) kernel, also called the Gaussian kernel, measures similarity by distance instead: two points that are close score near `1`, and points far apart score near `0`. A classifier built on it can carve out curved, island-shaped regions that no hyperplane could.

Given `X` with shape `(n, d)` and `Y` with shape `(m, d)`, return the `(n, m)` matrix of RBF similarities with a width parameter `gamma`.

### Constraints

- Return an array of shape `(n, m)` where entry `[i, j]` equals `exp(-gamma * ||X[i] - Y[j]||^2)`.
- `gamma` defaults to `1.0`.
- Every entry must be finite, including the diagonal of `rbf_kernel(X, X)`, which must be exactly `1` up to floating point error.
- Do not modify `X` or `Y`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Squared distance expands as `||x||^2 + ||y||^2 - 2 x.y`. That expansion gives the whole matrix from three pieces, with no double loop.

</details>

<details>
<summary>Hint 2</summary>

Floating point rounding can make a squared distance slightly negative for identical points, which would push `exp` above `1`. Clip the squared distances at zero before exponentiating.

</details>

## Theory

### The simple version

Picture each training point as the center of a soft bump. The similarity between a new point and a training point is how tall that bump is at the new point's location: full height when they coincide, fading smoothly as they move apart. `gamma` sets how quickly the bump fades. A large `gamma` makes narrow bumps that only respond to very close neighbors, and a small `gamma` makes wide, gentle bumps.

### The formula

$$
k_{\text{rbf}}(x, y) = \exp\left(-\gamma \lVert x - y \rVert^2\right)
$$

Every pairwise squared distance comes from one identity, which is what keeps the computation vectorized:

$$
\lVert x - y \rVert^2 = \lVert x \rVert^2 + \lVert y \rVert^2 - 2\, x^\top y
$$

## Explanation

`rbf_kernel` computes the squared norm of each row of `X` and `Y`, combines them with the cross term `X @ Y.T` using the identity from Theory, clips tiny negative values from rounding at zero, and applies `exp(-gamma * sq_dist)`. The clip is what keeps identical points at exactly `1` instead of a value that drifts above it.
