---
name: unsupervised-kmeans-assignment
title: 'K-Means: assignment step'
tags: [classical-ml, unsupervised, clustering, kmeans]
difficulty: Beginner
---

## Statement

Implement:

```python
def kmeans_assign(input: np.ndarray, centroids: np.ndarray) -> np.ndarray:
    """Returns shape (n_samples,): index of the nearest centroid per sample."""
```

- Reuse `01-knn`'s `pairwise_distances`, don't recompute distances by hand.

## Theory

`04-nearest-centroid` predicted a _known_ class by finding the nearest of several fixed, pre-computed centroids. K-Means turns that same nearest-centroid idea into an unsupervised algorithm: there are no known classes at all, just `k` centroids that start at arbitrary positions and get refined by alternating two steps:

```text
1. Assignment step (this question): assign every point to its nearest centroid
2. Update step (02-kmeans-centroid-update): move each centroid to the mean of the points now assigned to it
   ... repeat until assignments stop changing
```

This question is exactly step 1, structurally identical to `04-nearest-centroid`'s prediction step, the only difference is that "which class is this point" isn't the question, "which cluster is this point currently closest to" is, and the centroids themselves aren't fixed, they'll move in the next step.

## Explanation

`kmeans_assign` calls `pairwise_distances(centroids, input)`, exactly the same call `04-nearest-centroid`'s `nearest_centroid_predict` makes, returning shape `(n_samples, k)`, every sample's distance to every centroid. `np.argmin(distances, axis=1)` picks the index of the closest centroid for each sample, ties resolve to the lower-indexed centroid (the first occurrence of the minimum), the same convention `np.argmax`-based tie-breaks use elsewhere in this curriculum.
