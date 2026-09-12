---
name: instance-based-probabilistic-knn
title: 'KNN: distance and neighbor lookup'
tags: [classical-ml, instance-based, knn]
difficulty: Beginner
---

## Statement

Implement:

```python
def pairwise_distances(input: np.ndarray, queries: np.ndarray) -> np.ndarray:
    """shape (n_queries, n_samples): Euclidean distance, every query to every sample."""

def knn_predict(input: np.ndarray, labels: np.ndarray, queries: np.ndarray, k: int) -> np.ndarray:
    """shape (n_queries,): majority class among each query's k nearest neighbors."""
```

- One vectorized expression for `pairwise_distances`, no loop over samples or queries.
- Ties in the vote are broken by the lower class label, same convention `01-random-forest-majority-vote` uses.

## Theory

Every model so far in this curriculum learns a fixed set of parameters (`weight`/`bias`, or a tree's structure) once, from the training data, then throws the training data away and uses only those parameters to predict. K-Nearest Neighbors does the opposite: it doesn't learn anything at training time, "training" is just storing `input`/`labels`, and every prediction re-examines the entire training set from scratch.

To predict a new point, find the `k` training points closest to it (by Euclidean distance, the straight-line distance in feature space), and vote: whichever class is most common among those `k` neighbors is the prediction. The reasoning is simple and intuitive: points near each other in feature space tend to share a label, so look at what your neighbors are.

```text
query point
   ↓ measure distance to every training point
k closest training points
   ↓ majority vote among their labels
prediction
```

This makes KNN "instance-based" (or "lazy"): there's no model to fit, no loss to minimize, no gradient to compute, the entire "model" is the training data itself plus a rule for using it at prediction time. The tradeoff is prediction cost: every single query has to compare itself against every training point, which doesn't scale the way a fitted `weight`/`bias` pair or even a tree does.

## Explanation

`pairwise_distances` computes every query-to-sample distance in one vectorized shot: `queries[:, np.newaxis, :]` has shape `(n_queries, 1, n_features)`, `input[np.newaxis, :, :]` has shape `(1, n_samples, n_features)`, subtracting them broadcasts to `(n_queries, n_samples, n_features)`, one difference vector for every query-sample pair. Squaring, summing over the last axis, and taking the square root collapses that down to `(n_queries, n_samples)`, exactly the standard Euclidean distance formula, computed for every pair simultaneously.

`knn_predict` calls `np.argsort(distances, axis=1)[:, :k]`, sorting each query's row of distances and keeping the first `k` column indices, the `k` nearest training points for that query. `labels[nearest_indices[i]]` looks up those neighbors' labels, and the majority-vote pattern (`np.unique` + `np.argmax`) is the exact same one `01-random-forest-majority-vote` uses, a vote among a handful of nearby labels instead of a vote among several trees' predictions, the same underlying idea either way.
