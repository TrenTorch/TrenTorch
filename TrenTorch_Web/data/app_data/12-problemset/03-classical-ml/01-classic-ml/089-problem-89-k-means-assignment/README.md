---
name: problem-89-k-means-assignment
title: 'K-Means Assignment'
tags: [problemset, unsupervised-ml, k-means-clustering]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'k-means clustering'
hint: 'argmin over centroids of the squared distance'
tools: [NumPy]
---

## Statement

Assign each point to its nearest centroid using squared Euclidean distance. A point equidistant from several centroids goes to the one with the lowest index.

Implement `solve(X,C)`.

**Returns.** Return an integer NumPy array of length `n_points` with the index of the nearest centroid for each point.

### Examples

**Example 1**

Input:

```python
solve([[0.0, 0.0], [2.0, 2.0], [1.0, 1.0]], [[0.0, 0.0], [3.0, 3.0]])
```

Output:

```text
[0, 1, 0]
```

**Example 2**

Input:

```python
solve([[0.0], [1.0]], [[0.0], [1.0], [5.0]])
```

Output:

```text
[0, 1]
```

## Theory

### The simple version

The assignment step of k-means is nearest-neighbour search against only $K$ points: every sample joins the cluster whose centre is closest to it.

### The rule

$$c_i=\arg\min_{k}\;\|x_i-\mu_k\|^2$$

## Explanation

Broadcasting builds an `(n_points, K, d)` array of differences, which is summed over the feature axis to give all squared distances at once. `argmin` returns the first minimum, so ties go to the lower centroid index.
