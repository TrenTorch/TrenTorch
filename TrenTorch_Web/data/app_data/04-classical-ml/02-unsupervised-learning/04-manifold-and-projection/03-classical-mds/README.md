---
name: manifold-classical-mds
title: 'Classical MDS'
tags: [classical-ml, unsupervised, mds, dimensionality-reduction]
difficulty: Intermediate
---

## Statement

### Coordinates from distances alone

Multidimensional scaling starts from a matrix of pairwise distances and looks for points whose distances match. Classical MDS solves this exactly when the distances are Euclidean.

Implement `classical_mds(D, k)`. Return coordinates of shape `(n, k)`.

1. Square the distances: S = D ∘ D (element-wise).
2. Double-center: B = −½ J S J, where J = I − (1/n) 11ᵀ.
3. Take the eigendecomposition of B. Keep the `k` largest eigenvalues.
4. Coordinates are the eigenvectors times the square roots of their eigenvalues. A negative eigenvalue contributes a zero column.

### Constraints

- `D` must be square, symmetric, with a zero diagonal, otherwise raise `ValueError`.
- `1 ≤ k ≤ n`, otherwise raise `ValueError`.
- Do not modify `D`.

### Hints

<details>
<summary>Hint 1</summary>

Write the centering as `J @ S @ J` with `J = np.eye(n) - np.ones((n, n)) / n`.

</details>

## Theory

For points in Euclidean space, B equals the Gram matrix of the centered points, so its eigendecomposition recovers the coordinates up to rotation and reflection. Distances are the only information used, so the embedding is only determined up to those symmetries.

## Explanation

The solution squares and double-centers the distance matrix, reads off the top eigenpairs, and scales the eigenvectors. Clamping negative eigenvalues keeps the output real when the distances are not perfectly Euclidean.
