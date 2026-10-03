---
name: unsupervised-fuzzy-c-means
title: 'Fuzzy c-means'
tags: [classical-ml, unsupervised, clustering, fuzzy]
difficulty: Intermediate
---

## Statement

### Soft memberships instead of hard labels

k-means assigns each point to exactly one cluster. Fuzzy c-means gives every point a membership in every cluster, with memberships that sum to 1. Points between two groups get split membership rather than a forced choice.

Implement `fuzzy_c_means(X, c, m=2.0, max_iter=100, tol=1e-5)`. Return `(centers, U)`, where `centers` has shape `(c, d)` and `U` has shape `(n, c)`.

1. Initialize centers with farthest-first picks: row 0, then repeatedly the row farthest from the chosen centers.
2. Membership update: u(i, k) = 1 / Σ over j of (d(i, k) / d(i, j))^(2 / (m − 1)), where d is Euclidean distance.
3. If a point sits exactly on a center (distance 0), its membership is 1 for that center and 0 for the others.
4. Center update: v(k) = Σ over i of u(i, k)^m · x(i) divided by Σ over i of u(i, k)^m.
5. Stop when the largest change in `U` is below `tol`, or after `max_iter` rounds.

### Constraints

- `m` must be greater than 1, otherwise raise `ValueError`.
- `1 ≤ c ≤ n`, otherwise raise `ValueError`.
- Each row of `U` sums to 1 and is nonnegative.
- Do not modify `X`.

### Hints

<details>
<summary>Hint 1</summary>

Compute the full distance matrix first with broadcasting, then handle zero distances with a mask before dividing.

</details>

<details>
<summary>Hint 2</summary>

For the center update, use the weights `U ** m` as a matrix and multiply by `X`.

</details>

## Theory

Fuzzy c-means minimizes Σ over i and k of u(i, k)^m · d(i, k)^2. The fuzzifier m controls softness: as m approaches 1 the memberships become nearly hard, and larger m spreads them out.

## Explanation

The solution alternates membership and center updates until memberships stop changing. Zero distances are handled explicitly so the membership formula never divides by zero, and rows are normalized implicitly by the formula itself.
