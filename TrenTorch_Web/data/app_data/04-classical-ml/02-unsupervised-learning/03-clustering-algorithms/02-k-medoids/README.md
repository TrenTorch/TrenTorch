---
name: unsupervised-k-medoids
title: 'k-medoids (alternating)'
tags: [classical-ml, unsupervised, clustering, robust]
difficulty: Advanced
---

## Statement

### The problem, from first principles

k-means represents each cluster by its mean, and a single outlier can drag a mean far away. k-medoids represents each cluster by one of its actual data points, the medoid that minimizes total distance to the other members. Because the center is always a real point, it is less affected by outliers, and it works with any distance function.

Implement `k_medoids(X, k, max_iter=100, seed=0)`, which returns `(labels, medoid_indices)`. Use Euclidean distance.

1. Pick k distinct medoid indices uniformly at random with `np.random.default_rng(seed)`.
2. Assign every point to its nearest medoid. The medoid point is assigned to its own cluster.
3. For each cluster, make the member that minimizes the sum of distances to the other members its new medoid. An empty cluster keeps its old medoid.
4. Repeat steps 2 and 3 until the medoids stop changing or `max_iter` is reached.

### Constraints

- `1 <= k <= n`, otherwise raise `ValueError`.
- `labels[medoid_indices[c]] == c` for every cluster `c`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Compute the full pairwise distance matrix once. Then assignment is `argmin` over the medoid columns.

</details>

<details>
<summary>Hint 2</summary>

Inside a cluster, use `D[np.ix_(members, members)].sum(axis=1)`. Its `argmin` gives the new medoid position.

</details>

## Theory

### The simple version

Pick real points as cluster centers, group every point with its closest center, then move each center to the member that is most central to its group. Repeat until nothing moves.

### The formula

$$
m_c = \arg\min_{i \in C_c} \sum_{j \in C_c} \lVert x_i - x_j \rVert
$$

## Explanation

`k_medoids` precomputes the distance matrix, assigns points by `argmin` over medoid columns, and updates each medoid by minimizing the within-cluster distance sum. Keeping the old medoid for an empty cluster prevents a crash and lets the loop converge.
