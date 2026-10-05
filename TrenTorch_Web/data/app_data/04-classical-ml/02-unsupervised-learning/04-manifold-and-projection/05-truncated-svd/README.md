---
name: manifold-truncated-svd
title: 'Truncated SVD'
tags: [classical-ml, unsupervised, svd, low-rank]
difficulty: Intermediate
---

## Statement

### Best low-rank approximation

Keeping only the top singular triplets of a matrix gives the closest rank-k matrix in Frobenius norm (Eckart-Young). Truncated SVD is the workhorse behind latent semantic analysis and many recommenders because it never forms a centered copy of the data.

Implement `truncated_svd(X, k)`. Return `(U_k, s_k, Vt_k)`, where `U_k` is `(n, k)`, `s_k` has length `k`, and `Vt_k` is `(k, d)`.

1. Compute the thin SVD of `X` with `np.linalg.svd(X, full_matrices=False)`.
2. Keep the first `k` columns of `U`, the first `k` singular values, and the first `k` rows of `Vt`.
3. Singular values come back in descending order and must stay that way.

Do not center the data. Truncated SVD works on the matrix as given.

### Constraints

- `1 ≤ k ≤ min(n, d)`, otherwise raise `ValueError`.
- Do not modify `X`.

## Theory

The residual of the rank-k approximation has squared Frobenius norm equal to the sum of the squared singular values beyond the first k. Reconstructing from the kept triplets therefore gives an error equal to the next singular value in the Frobenius sense when the matrix has rank k + 1.

## Explanation

The solution takes the thin SVD and slices the leading triplets. Skipping centering keeps this distinct from PCA, which is a deliberate point of the question.
