---
name: manifold-zca-whitening
title: 'ZCA whitening'
tags: [classical-ml, unsupervised, whitening, preprocessing]
difficulty: Intermediate
---

## Statement

### Decorrelate without rotating the data

Whitening makes features uncorrelated with unit variance. PCA whitening does this by rotating into the principal axes, which can make images look unlike the original. ZCA whitening applies the same decorrelation but rotates back, so the output stays as close to the input as a whitening transform can be.

Implement `zca_whiten(X, eps=1e-8)`. Return an array of the same shape as `X`.

1. Center the columns of `X`.
2. Compute the sample covariance C = Xᵀ X / (n − 1).
3. Take the eigendecomposition C = V Λ Vᵀ.
4. Build the whitening matrix W = V diag(1 / sqrt(λ + eps)) Vᵀ.
5. Return X_centered · W.

### Constraints

- `X` must have at least 2 rows, otherwise raise `ValueError`.
- `eps` must be nonnegative, otherwise raise `ValueError`.
- Do not modify `X`.

### Hints

<details>
<summary>Hint 1</summary>

With `eigh` the matrix `V diag(...) Vᵀ` is symmetric, so you can build it with `vecs * scale @ vecs.T`.

</details>

## Theory

Any whitening transform W satisfies Wᵀ C W = I. Those transforms differ by a rotation, and ZCA is the choice that minimizes the distance between the whitened data and the centered original.

## Explanation

The solution centers, forms the covariance, and builds the symmetric whitening matrix from the eigendecomposition. Adding `eps` inside the square root keeps near-zero variances from exploding.
