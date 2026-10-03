---
name: unsupervised-kmeans-plus-plus-init
title: 'k-means++ initialization'
tags: [classical-ml, unsupervised, clustering, kmeans]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Plain k-means picks starting centers uniformly at random, and bad luck can drop two starting centers into the same blob. The run then converges to a poor local optimum. k-means++ spreads the starting centers out: the first center is random, and each later center is chosen with probability proportional to its squared distance from the nearest center already picked. Far-away points are likelier, so new centers land in unexplored regions.

Implement `kmeans_plus_plus_init(X, k, seed=0)`, which returns a `(k, d)` array whose rows are chosen points from `X`.

1. Pick the first center uniformly at random.
2. For each next center, compute D² for every point (squared distance to the nearest chosen center) and sample a point with probability D² / ΣD².
3. If every D² is zero (all remaining points coincide with a center), pick uniformly at random.

### Constraints

- `1 <= k <= n`, otherwise raise `ValueError`.
- The same `seed` must give the same centers.
- Do not modify `X`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Keep a list of chosen indices. Update a running `d2` array with `np.minimum` after each new center.

</details>

<details>
<summary>Hint 2</summary>

`rng.choice(n, p=d2 / d2.sum())` samples the next index. Guard against an all-zero `d2` first.

</details>

## Theory

### The simple version

Choose each new starting center with odds that favor points far from the ones you already have. The result is a spread-out start, which is what k-means needs to avoid a bad local optimum.

### The formula

$$
P(x) = \frac{D(x)^2}{\sum_{x'} D(x')^2}, \qquad D(x) = \min_{c \in \text{chosen}} \lVert x - c \rVert
$$

## Explanation

`kmeans_plus_plus_init` keeps a running minimum of squared distances to the chosen centers and samples the next index in proportion to it. Points already chosen have zero distance, so they can never be picked twice unless every point coincides.
