---
name: unsupervised-clustering-adjusted-rand
title: 'Adjusted Rand index'
tags: [classical-ml, unsupervised, clustering, evaluation]
difficulty: Advanced
---

## Statement

### The problem, from first principles

When you have ground-truth labels, you can compare a clustering with them. The raw Rand index counts pairs of points that agree (both together or both apart), but random clusterings already agree on many pairs, so the raw score looks high by chance. The adjusted Rand index corrects for that: 0 means chance-level agreement, 1 means identical partitions, and negative values mean worse than chance.

Implement `adjusted_rand_index(labels_true, labels_pred)`.

1. Build the contingency table n_ij = number of points in true cluster i and predicted cluster j.
2. Let a_i and b_j be the row and column totals, and N the number of points.
3. ARI = (Σ C(n_ij, 2) − [Σ C(a_i, 2) · Σ C(b_j, 2)] / C(N, 2)) / (½[Σ C(a_i, 2) + Σ C(b_j, 2)] − [Σ C(a_i, 2) · Σ C(b_j, 2)] / C(N, 2)).

### Constraints

- Inputs must have the same length, otherwise raise `ValueError`.
- If the two partitions are both trivial (one cluster each, or every point alone), return `1.0`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.unique(..., return_inverse=True)` turns arbitrary labels into contiguous indices, which makes the contingency table a single `np.add.at` call.

</details>

<details>
<summary>Hint 2</summary>

Use `comb(x, 2) = x * (x - 1) / 2`, which works on numpy arrays. The denominator becomes zero only for trivial partitions.

</details>

## Theory

### The simple version

Count how many pairs of points two clusterings agree on, then subtract the agreement you would expect if the clusterings were unrelated, and rescale so the best possible score is 1.

### The formula

$$
\text{ARI} = \frac{\sum_{ij}\binom{n_{ij}}{2} - \frac{\sum_i \binom{a_i}{2}\sum_j \binom{b_j}{2}}{\binom{N}{2}}}{\tfrac12\left[\sum_i \binom{a_i}{2} + \sum_j \binom{b_j}{2}\right] - \frac{\sum_i \binom{a_i}{2}\sum_j \binom{b_j}{2}}{\binom{N}{2}}}
$$

## Explanation

`adjusted_rand_index` maps both labelings to contiguous indices, fills the contingency table, and evaluates the three pair-count sums. The chance term `expected` is what the raw Rand index loses, and subtracting it is the whole adjustment.
