---
name: unsupervised-kmeans-centroid-update
title: 'K-Means: centroid update'
tags: [classical-ml, unsupervised, clustering, kmeans]
difficulty: Beginner
---

## Statement

Implement:

```python
def kmeans_update_centroids(input, assignments, centroids) -> np.ndarray:
    """Returns shape (k, n_features): each centroid moved to the mean of its assigned points."""
```

- A cluster with zero points assigned to it keeps its old centroid unchanged, don't average an empty group.

## Theory

`01-kmeans-assignment` answered "which centroid is each point closest to right now." This question is the other half of one K-Means iteration: given those assignments, move each centroid to the actual center of the points now assigned to it, `04-nearest-centroid`'s centroid computation, applied per cluster instead of per class.

```text
1. Assignment step (01-kmeans-assignment): assign every point to its nearest centroid
2. Update step (this question): move each centroid to the mean of its assigned points
   ... repeat until centroids stop moving (or stop changing enough)
```

Repeating these two steps is the entire K-Means algorithm, no gradient, no loss function differentiated by hand, each step alone is simple, alternating them until convergence is what clusters the data.

The empty-cluster case matters because it's a real possibility, not a hypothetical: a poorly-initialized centroid can end up farther from every point than every other centroid is, meaning the assignment step never assigns it anything. Averaging zero points is undefined (`0/0`), leaving that centroid exactly where it was is the standard, simplest fix, it stays a candidate for the next iteration's assignment step rather than vanishing or crashing the algorithm.

## Explanation

`kmeans_update_centroids` starts from `centroids.copy()`, not the original array, downstream code that still holds a reference to the old `centroids` shouldn't see it silently mutated. For each cluster index, `input[assignments == cluster]` selects exactly the rows currently assigned to it, and `.mean(axis=0)` averages them per feature, replacing that row of `new_centroids`. The `if members.shape[0] > 0` guard is the empty-cluster case: skip the update entirely, leaving that row exactly as it was copied from `centroids`.
