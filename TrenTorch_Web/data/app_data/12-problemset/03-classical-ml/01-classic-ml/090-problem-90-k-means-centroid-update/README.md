---
name: problem-90-k-means-centroid-update
title: 'K-Means Centroid Update'
tags: [problemset, unsupervised-ml, k-means-clustering]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'k-means clustering'
hint: 'for each k, the mean of the rows with label k (zeros if none)'
tools: [NumPy]
---

## Statement

Recompute k-means centroids from cluster labels. `labels[i]` in $\{0,\dots,K-1\}$ gives the cluster of row `X[i]`; each centroid is the mean of its cluster's points. A cluster with no points gets the zero vector.

Implement `solve(X,labels,K)`.

**Returns.** Return a `(K, d)` float NumPy array of centroids.

### Examples

**Example 1**

Input:

```python
solve([[0.0, 0.0], [2.0, 0.0], [10.0, 10.0]], [0, 0, 1], 2)
```

Output:

```text
[[1.0, 0.0], [10.0, 10.0]]
```

**Example 2**

Input:

```python
solve([[1.0, 1.0], [3.0, 3.0]], [0, 0], 3)
```

Output:

```text
[[2.0, 2.0], [0.0, 0.0], [0.0, 0.0]]
```

## Theory

### The simple version

The update step of k-means moves each centre to the average of the points currently assigned to it. This is the choice of centre that minimises the sum of squared distances to those points.

### The formula

$$\mu_k=\frac1{|C_k|}\sum_{i\in C_k}x_i$$

## Explanation

A cluster that lost all its points has no mean, so this implementation returns zeros for it (in the second example clusters 1 and 2 are empty). The next problem shows the other common convention of keeping the old centroid.
