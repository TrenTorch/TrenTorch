---
name: instance-based-probabilistic-nearest-centroid
title: Nearest centroid classifier
tags: [classical-ml, instance-based]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`01-knn` predicts by comparing a query against *every* training point — accurate, but the prediction cost grows with the size of the training set. Nearest centroid asks whether that's really necessary: if a class's points cluster together, a single summary point per class (its centroid) might capture "what this class looks like" well enough to skip comparing against every individual training example.

### From theory to code

Implement `nearest_centroid_fit(input, labels)`, which returns one centroid per class, and `nearest_centroid_predict(model, queries)`, which assigns each query to its nearest centroid's class. Reuse `01-knn`'s `pairwise_distances` — don't recompute distances by hand.

### Constraints

- `nearest_centroid_fit` returns `{"classes": ..., "centroids": array (n_classes, n_features)}`, one centroid row per distinct class, in the same order as `classes`.
- A centroid is the mean feature vector of that class's own training rows.
- `nearest_centroid_predict` returns one predicted class per row of `queries`, the class of the nearest centroid (Euclidean distance).
- Ties broken toward the lower class label (whichever `np.argmin` returns first).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

A list comprehension over `np.unique(labels)`, each computing `input[labels == c].mean(axis=0)`, stacked with `np.array(...)`, is the whole fit step.

</details>

<details>
<summary>Hint 2</summary>

`pairwise_distances` doesn't care whether its first argument is "real" training points or centroids — pass the fitted centroids in as if they were the training set, and it returns `(n_queries, n_classes)` distances directly.

</details>

## Theory

### The simple version

`01-knn` compares a query against *every* training point. Nearest centroid compares a query against just one summary point per class — that class's centroid, the mean position of all its training examples. Whichever centroid is closest wins.

### The formula

```text
training data
   -> group by class, average each group
one centroid per class
   -> measure distance from a new query to every centroid
prediction = the class of the nearest one
```

This is a genuinely different tradeoff from KNN: nearest centroid is cheap at prediction time (compare against `n_classes` centroids, not all `n_samples` training points) and cheap to update (recomputing a mean is fast), but it assumes each class forms roughly one compact blob — it has no way to represent a class shaped like two separate clusters, a single centroid would sit in the empty space between them. KNN makes no such assumption, at the cost of comparing against every training point every time.

### How PyTorch actually implements this

Context only, untested by your submission: this is a classical statistical model, not a PyTorch operation — the closest real-world equivalent is scikit-learn's `NearestCentroid`, which computes exactly this per-class mean and nearest-centroid assignment.

## Explanation

`nearest_centroid_fit` computes `input[labels == c].mean(axis=0)` for every distinct class `c` — the average feature vector of that class's own training rows, stacked into one `(n_classes, n_features)` array in the same order as `classes`.

`nearest_centroid_predict` calls `pairwise_distances(model["centroids"], queries)`, treating the centroids themselves as if they were "training points" — this returns shape `(n_queries, n_classes)`, distance from every query to every centroid. `np.argmin(distances, axis=1)` picks the nearest centroid's index for each query, and indexing `model["classes"]` with those indices turns "which centroid" back into "which class."
