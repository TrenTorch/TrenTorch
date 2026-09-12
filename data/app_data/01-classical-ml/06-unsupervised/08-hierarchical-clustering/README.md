---
name: unsupervised-hierarchical-clustering
title: 'Hierarchical clustering: agglomerative merge order'
tags: [classical-ml, unsupervised, clustering, hierarchical]
difficulty: Intermediate
---

## Statement

Implement:

```python
def cluster_distance(points_a: np.ndarray, points_b: np.ndarray, linkage: str) -> float: ...
def agglomerative_fit(input: np.ndarray, n_clusters: int, linkage: str = "single") -> np.ndarray: ...
```

- `linkage` is `'single'`, `'complete'`, or `'average'`, anything else raises `ValueError`.
- Reuse `01-knn`'s `pairwise_distances`.

## Theory

K-Means, GMM, and DBSCAN each build clusters by some form of "which points does this cluster currently claim." Agglomerative (bottom-up) hierarchical clustering builds clusters the opposite way: start with every point as its _own_ cluster, then repeatedly merge the two closest clusters into one, until only `n_clusters` remain.

```text
n singleton clusters
   ↓ merge the two closest clusters
n-1 clusters
   ↓ merge the two closest clusters
n-2 clusters
   ...
n_clusters clusters (stop here)
```

"Closest clusters" needs a definition once clusters have more than one point each, that's **linkage**:

- **single**: the distance between the closest pair of points, one from each cluster. Tends to chain together long, thin, snake-like clusters.
- **complete**: the distance between the farthest pair of points, one from each cluster. Tends to produce tight, compact, roughly equal-sized clusters.
- **average**: the mean distance across every pair, one from each cluster. A middle ground between the two.

The same two clusters can have a very different "distance" depending on which linkage is used, which is why the choice matters and isn't just an implementation detail.

## Explanation

`cluster_distance` computes the full pairwise distance matrix between the two groups (`pairwise_distances(points_a, points_b)`), then reduces it with `.min()`, `.max()`, or `.mean()` depending on `linkage`, the three definitions above, applied directly.

`agglomerative_fit` represents `clusters` as a plain Python list of index lists (`clusters[k]` is the list of original row indices currently in cluster `k`), not a NumPy array, since clusters merge and shrink in count as the algorithm runs. Each iteration scans every pair of current clusters (`for a in range(len(clusters)): for b in range(a+1, len(clusters))`), computing `cluster_distance` on the actual rows (`input[clusters[a]]`, `input[clusters[b]]`) each time, and merges whichever pair is closest: `clusters[a] = clusters[a] + clusters[b]` absorbs `b`'s members into `a`, then `del clusters[b]` removes the now-redundant entry. This repeats until exactly `n_clusters` remain, at which point every remaining cluster's members get labeled with that cluster's position in the final list.
