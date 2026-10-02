---
name: unsupervised-rand-index
title: Rand index
tags: [classical-ml, clustering, performance-measure]
difficulty: Beginner
---

## Statement

### The problem, from first principles

If you do have reference labels, you can ask how well a clustering agrees with them. Cluster ids are arbitrary names, so comparing them directly is meaningless; instead compare how both partitions treat every _pair_ of samples: together in both, or apart in both, counts as agreement.

### From theory to code

Implement `rand_index(labels_a, labels_b)`, the fraction of sample pairs on which the two partitions agree.

### Constraints

- `labels_a` and `labels_b` are one-dimensional arrays of equal length; ids can be any integers.
- A pair agrees if both partitions put it in the same cluster, or both put it in different clusters.
- Return a Python `float` in `[0, 1]`; return `1.0` when there are fewer than two samples (no pairs).

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Build an `n x n` boolean matrix per partition saying whether two samples share a cluster: `a[:, None] == a[None, :]`.

</details>

<details><summary>Hint 2</summary>

Compare the two matrices on the upper triangle only (`np.triu_indices(n, k=1)`) so each pair counts once and no sample is paired with itself.

</details>

## Theory

### The simple version

Two clusterings can be identical yet use different names for their clusters. The Rand index ignores names and just checks, pair by pair, whether the two clusterings tell the same story.

### The formula

$$\text{RI} = \frac{a + d}{\binom{n}{2}}$$

where $a$ counts pairs together in both partitions and $d$ counts pairs apart in both.

### How libraries implement this

`sklearn.metrics.rand_score` computes this; `adjusted_rand_score` subtracts the agreement expected by chance.

## Explanation

Only the upper triangle is compared so each unordered pair counts once. Because it only uses equality of ids within each partition, any relabeling of clusters leaves the result unchanged.
