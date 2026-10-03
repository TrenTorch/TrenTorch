---
name: feature-selection-orthogonal-matching-pursuit
title: 'Orthogonal matching pursuit'
tags: [classical-ml, feature-selection, sparse-learning, compressed-sensing, greedy]
difficulty: Advanced
---

## Statement

### Explain a signal with as few atoms as possible

Given a dictionary `D` whose columns are candidate features (or atoms), and a target `y`, we want a coefficient vector with only a few nonzero entries. Orthogonal matching pursuit (OMP) builds that support one column at a time.

Implement `omp(D, y, k)`. It returns a coefficient vector of length `d` with at most `k` nonzero entries.

1. Start with an empty support and residual `r = y`.
2. Pick the column with the largest absolute inner product `|D^T r|` among columns not yet selected. Ties go to the smallest index.
3. Solve least squares of `y` on the selected columns. Update the residual to `y - D_S x_S`.
4. Repeat `k` times, then write the least-squares coefficients into their positions.

### Constraints

- `D` is 2-D with `n` rows, `y` has length `n`.
- `0 <= k <= d`, otherwise raise `ValueError`.
- `k = 0` returns all zeros.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Set the correlation of already-selected columns to negative infinity before the `argmax`, so they cannot be picked twice.

</details>

## Theory

Each new column is orthogonal to the current residual's fit, so the residual is orthogonal to every selected column afterwards. For a dictionary with incoherent columns, OMP recovers a true sparse signal exactly from noise-free measurements when the sparsity is small enough. That is the core idea behind compressed sensing.

### Where this shows up in production

Sparse signal recovery in compressed sensing pipelines, such as reconstructing an image or audio segment from a few measurements against a fixed dictionary. It also appears as a fast approximation to best-subset selection when a model needs a hard limit on the number of active features.

### Using it to make decisions

Use it when the dictionary columns are close to orthogonal and you know a sparsity budget k in advance. Check coherence between columns first. When two columns are nearly identical, OMP can pick the wrong one at the first step and never recover, so the support it returns is not trustworthy. If k is unknown, pick it with a held-out reconstruction error curve and stop where the curve flattens.

### Pros and cons

**Pros:** fast (k least-squares fits), deterministic, a clear stopping rule, and it recovers the true support exactly under standard incoherence conditions.

**Cons:** no optimality guarantee, k must be chosen up front, and it is fragile when columns are correlated. The refit at every step makes the cost grow with k.

## Explanation

The solution keeps the support as a list, re-fits with `lstsq` after every addition, and recomputes the residual. Masking selected columns with negative infinity keeps the `argmax` honest.
