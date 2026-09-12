---
name: unsupervised-hierarchical-clustering
title: 'Hierarchical clustering: agglomerative merge order'
tags: [classical-ml, unsupervised, clustering, hierarchical]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

K-Means, GMM, and DBSCAN each build clusters by some form of "which points does this cluster currently claim," starting from some notion of cluster centers or dense regions. Agglomerative (bottom-up) hierarchical clustering takes the opposite approach entirely: start with every point as its *own* cluster, and repeatedly merge whichever two clusters are closest, until only the desired number remain.

### From theory to code

Implement `cluster_distance(points_a, points_b, linkage)` and `agglomerative_fit(input, n_clusters, linkage="single")`. `linkage` is `'single'`, `'complete'`, or `'average'` — anything else raises `ValueError`. Reuse `01-knn`'s `pairwise_distances`.

### Constraints

- `cluster_distance` computes the distance between two groups of points under the given linkage: `'single'` (closest pair), `'complete'` (farthest pair), `'average'` (mean over all pairs).
- An unrecognized `linkage` raises `ValueError`.
- `agglomerative_fit` starts with every row as its own cluster and repeatedly merges the two closest (by `cluster_distance`) until exactly `n_clusters` remain.
- Returns one cluster id per row, consistent within a merged group.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`cluster_distance` is one full pairwise distance matrix between the two groups, reduced by `.min()`, `.max()`, or `.mean()` depending on `linkage` — no need to loop over pairs by hand.

</details>

<details>
<summary>Hint 2</summary>

Represent `clusters` as a plain Python list of index lists, not a NumPy array — the number of clusters shrinks every iteration, and each cluster's member count varies, which a ragged list handles naturally.

</details>

## Theory

### The simple version

K-Means, GMM, and DBSCAN each build clusters by some form of "which points does this cluster currently claim." Agglomerative (bottom-up) hierarchical clustering builds clusters the opposite way: start with every point as its *own* cluster, then repeatedly merge the two closest clusters into one, until only `n_clusters` remain.

```text
n singleton clusters
   -> merge the two closest clusters
n-1 clusters
   -> merge the two closest clusters
n-2 clusters
   ...
n_clusters clusters (stop here)
```

### The formula

"Closest clusters" needs a definition once clusters have more than one point each — that's **linkage**:

- **single**: the distance between the closest pair of points, one from each cluster. Tends to chain together long, thin, snake-like clusters.
- **complete**: the distance between the farthest pair of points, one from each cluster. Tends to produce tight, compact, roughly equal-sized clusters.
- **average**: the mean distance across every pair, one from each cluster. A middle ground between the two.

The same two clusters can have a very different "distance" depending on which linkage is used, which is why the choice matters and isn't just an implementation detail.

### How PyTorch actually implements this

Context only, untested by your submission: this is a classical clustering algorithm, not a PyTorch operation — the real-world equivalent is scikit-learn's `AgglomerativeClustering`, which this exercise's own `tests.py` verifies against directly (`test_matches_real_sklearn_agglomerative_clustering_co_membership` checks the same permutation-invariant co-membership property — which points end up in the same cluster — that an `adjusted_rand_score` comparison against a real, fitted `sklearn.cluster.AgglomerativeClustering` confirmed offline).

## Explanation

`cluster_distance` computes the full pairwise distance matrix between the two groups (`pairwise_distances(points_a, points_b)`), then reduces it with `.min()`, `.max()`, or `.mean()` depending on `linkage` — the three definitions above, applied directly.

`agglomerative_fit` represents `clusters` as a plain Python list of index lists (`clusters[k]` is the list of original row indices currently in cluster `k`), not a NumPy array, since clusters merge and shrink in count as the algorithm runs. Each iteration scans every pair of current clusters (`for a in range(len(clusters)): for b in range(a+1, len(clusters))`), computing `cluster_distance` on the actual rows (`input[clusters[a]]`, `input[clusters[b]]`) each time, and merges whichever pair is closest: `clusters[a] = clusters[a] + clusters[b]` absorbs `b`'s members into `a`, then `del clusters[b]` removes the now-redundant entry. This repeats until exactly `n_clusters` remain, at which point every remaining cluster's members get labeled with that cluster's position in the final list.
