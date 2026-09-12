---
name: instance-based-probabilistic-nearest-centroid
title: Nearest centroid classifier
tags: [classical-ml, instance-based]
difficulty: Beginner
---

## Statement

Implement:

```python
def nearest_centroid_fit(input: np.ndarray, labels: np.ndarray) -> dict:
    """Returns {"classes": ..., "centroids": array (n_classes, n_features)}."""

def nearest_centroid_predict(model: dict, queries: np.ndarray) -> np.ndarray:
    """Returns the class of the nearest centroid to each query."""
```

- Reuse `01-knn`'s `pairwise_distances`, don't recompute distances by hand.

## Theory

`01-knn` compares a query against _every_ training point. Nearest centroid compares a query against just one summary point per class, that class's centroid, the mean position of all its training examples. Whichever centroid is closest wins.

```text
training data
   ↓ group by class, average each group
one centroid per class
   ↓ measure distance from a new query to every centroid
prediction = the class of the nearest one
```

This is a genuinely different tradeoff from KNN: nearest centroid is cheap at prediction time (compare against `n_classes` centroids, not all `n_samples` training points) and cheap to update (recomputing a mean is fast), but it assumes each class forms roughly one compact blob, it has no way to represent a class shaped like two separate clusters, a single centroid would sit in the empty space between them. KNN makes no such assumption, at the cost of comparing against every training point every time.

## Explanation

`nearest_centroid_fit` computes `input[labels == c].mean(axis=0)` for every distinct class `c`, the average feature vector of that class's own training rows, stacked into one `(n_classes, n_features)` array in the same order as `classes`.

`nearest_centroid_predict` calls `pairwise_distances(model["centroids"], queries)`, treating the centroids themselves as if they were "training points," this returns shape `(n_queries, n_classes)`, distance from every query to every centroid. `np.argmin(distances, axis=1)` picks the nearest centroid's index for each query, and indexing `model["classes"]` with those indices turns "which centroid" back into "which class."
