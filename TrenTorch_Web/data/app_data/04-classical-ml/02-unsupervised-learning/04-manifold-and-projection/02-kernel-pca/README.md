---
name: manifold-kernel-pca
title: 'Kernel PCA'
tags: [classical-ml, unsupervised, pca, kernel, dimensionality-reduction]
difficulty: Advanced
---

## Statement

### PCA in feature space

Plain PCA finds straight directions, so it cannot unfold curved structure. Kernel PCA runs PCA on a kernel matrix instead, which implicitly maps the data into a richer feature space.

Implement `kernel_pca(X, n_components, gamma=None)`. Return an array of shape `(n, n_components)`.

1. Build the kernel matrix K. If `gamma` is `None`, use the linear kernel K = X Xᵀ. Otherwise use the RBF kernel K(i, j) = exp(−gamma · ||x_i − x_j||²).
2. Center the kernel: Kc = K − 1ₙK − K1ₙ + 1ₙK1ₙ, where 1ₙ is the n × n matrix with entries 1/n.
3. Take the eigendecomposition of Kc. Keep the `n_components` largest eigenvalues with their eigenvectors.
4. Scores are the eigenvectors scaled by the square roots of their eigenvalues. Eigenvalues that are not positive contribute zero columns.

### Constraints

- `1 ≤ n_components ≤ n`, otherwise raise `ValueError`.
- `gamma` must be positive when given, otherwise raise `ValueError`.
- Do not modify `X`.

### Hints

<details>
<summary>Hint 1</summary>

`np.linalg.eigh` returns eigenvalues in ascending order. Reverse the last `n_components` columns to get the largest first.

</details>

## Theory

Centering in feature space is done with the kernel alone, so the explicit feature map never has to be computed. With the linear kernel, kernel PCA reduces to ordinary PCA, which gives a useful check.

## Explanation

The solution builds the kernel, centers it with the closed form, takes the top eigenpairs, and scales the eigenvectors. The linear case matches PCA scores up to sign, which the tests use as a reference.
