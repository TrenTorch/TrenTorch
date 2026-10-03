---
name: manifold-random-projection
title: 'Gaussian random projection'
tags: [classical-ml, unsupervised, random-projection, johnson-lindenstrauss]
difficulty: Intermediate
---

## Statement

### Cheap dimensionality reduction with distance guarantees

The Johnson-Lindenstrauss lemma says that a random linear map to roughly O(log n / ε²) dimensions preserves pairwise distances up to a factor (1 ± ε). A Gaussian random projection is the simplest such map, and it needs no training.

Implement `gaussian_random_projection(X, k, seed=0)`. Return an array of shape `(n, k)`.

1. Create a generator with `np.random.default_rng(seed)`.
2. Draw R of shape `(d, k)` with independent N(0, 1) entries, then divide by √k.
3. Return X · R.

### Constraints

- `k ≥ 1`, otherwise raise `ValueError`.
- The same seed must give the same output.
- Do not modify `X`.

## Theory

For a fixed pair of points, the squared distance after projection has expectation equal to the original squared distance because each column of R has variance 1/k per entry. The concentration bound is what makes the projection safe to use.

## Explanation

The solution draws the matrix with a seeded generator, scales it by 1/√k so expected squared norms are preserved, and multiplies. The tests check shape, determinism, and that average squared distances stay close on a fixed sample.
