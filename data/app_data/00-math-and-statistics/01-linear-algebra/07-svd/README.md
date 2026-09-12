---
name: math-svd
title: Singular Value Decomposition (SVD)
tags: [linear-algebra, matrices]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`06-eigenvalues-eigenvectors` only works for square matrices, but most real data isn't square: a dataset is `(num_samples, num_features)`, an image is `(height, width)`, neither is guaranteed to have equal dimensions. You still want the same kind of insight, "what are this matrix's most important directions, and can I throw away the unimportant ones", just without requiring squareness.

Singular Value Decomposition answers exactly that, for any matrix at all. And it comes with a genuinely useful guarantee: if you keep only the most important handful of directions it finds, you get the mathematically _best possible_ approximation of the original matrix at that size, not just a reasonable one.

### From theory to code

Theory gives the factorization `A = U @ diag(sigma) @ V^T` with singular values sorted descending by construction. Implement the factorization itself, a function that rebuilds the original from the three pieces, and a compression step that keeps only the top `k` singular values.

Implement `svd(a)`, `reconstruct_from_svd(u, singular_values, vt)` and `low_rank_approximation(a, k)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `a` is `(m, n)`, any shape, not required to be square.
- Use the reduced ("economy") form: `u` is `(m, r)`, `vt` is `(r, n)`, `r = min(m, n)`.
- `low_rank_approximation` keeps the top `k` singular values, since `np.linalg.svd` already sorts them descending, "top k" is just "first k", no explicit sorting needed.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.linalg.svd` with `full_matrices=False` returns exactly the three pieces this question asks for, in the shapes Theory describes.

</details>

<details>
<summary>Hint 2</summary>

`low_rank_approximation` is `svd` followed by slicing each of the three returned pieces down to their first `k` entries/columns/rows, then calling `reconstruct_from_svd` on the truncated pieces.

</details>

## Theory

### The simple version

A photograph is a big grid of pixel brightness values, but most of what makes it recognizable comes from a handful of dominant patterns, big regions of light and dark, not every individual pixel's exact value. SVD finds those dominant patterns directly, ranked by how much of the image they explain, so keeping only the top few and throwing away the rest still looks recognizably like the original.

### The formula

Eigendecomposition (`06-eigenvalues-eigenvectors`) only applies to square matrices. **Singular Value Decomposition** generalizes the same idea, "break a matrix into simpler pieces", to any matrix at all, square or rectangular:

```text
A = U @ diag(sigma) @ V^T
```

where `A` is `(m, n)`, `U` is `(m, r)` with orthonormal columns, `V^T` is `(r, n)` with orthonormal rows, and `sigma` (the **singular values**) is a length-`r` list of non-negative numbers sorted descending, `r = min(m, n)` in the "reduced" form this question uses.

The singular values measure how much "information" each direction of the decomposition carries, the largest singular value corresponds to the direction `A` stretches the most. This ordering is exactly what makes SVD useful for compression: keeping only the top `k` singular values (and their corresponding columns of `U` and rows of `V^T`) gives the best possible rank-`k` approximation of `A`, in the sense of minimizing squared reconstruction error (the Eckart-Young theorem). Truncating the smallest singular values throws away the directions that mattered least.

This is precisely the mechanism behind PCA (a later question in `06-unsupervised`): PCA's "find the top eigenvectors of the covariance matrix" is, in practice, almost always computed via SVD directly on the (centered) data matrix, without ever forming the covariance matrix at all.

### How PyTorch actually implements this

`torch.linalg.svd` dispatches to LAPACK's `gesdd` (divide-and-conquer SVD), the same family of algorithms real recommendation systems use for matrix factorization and real image compression pipelines use for low-rank approximation. `torch.svd_lowrank` goes further: rather than computing the _full_ SVD and then truncating (this question's approach, fine for small matrices), it uses randomized projection to approximate only the top `k` singular values/vectors directly, avoiding ever computing the parts you were going to throw away, essential once `m` and `n` are in the millions (a large embedding matrix, say) where a full SVD would be far too slow to run at all.

## Explanation

`svd` returns `np.linalg.svd(a, full_matrices=False)`, the reduced-form factorization from Theory.

`reconstruct_from_svd` rebuilds `u @ diag(singular_values) @ vt`, the direct definition.

`low_rank_approximation` computes the full SVD, then reconstructs using only the first `k` columns of `u`, the first `k` singular values, and the first `k` rows of `vt`, since `np.linalg.svd` already returns singular values sorted descending, "top k" is simply "first k".
