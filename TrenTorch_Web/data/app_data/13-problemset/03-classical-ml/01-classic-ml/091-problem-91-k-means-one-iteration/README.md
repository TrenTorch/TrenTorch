---
name: problem-91-k-means-one-iteration
title: 'K-Means One Iteration'
tags: [problemset, unsupervised-ml, k-means-clustering]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'k-means clustering'
hint: 'assign by argmin distance, then average each cluster (keep old centroid if empty)'
tools: [NumPy]
---

## Statement

Run one full k-means iteration: assign every point to its nearest centroid (squared Euclidean distance, lowest index on ties) and then move each centroid to the mean of its assigned points. A centroid that receives no points stays where it was.

Implement `solve(X, C)`.

**Returns.** Return a tuple `(labels, new_centroids)`: an integer array of length `n_points` and a `(K, d)` float array.

### Examples

**Example 1**

Input:

```python
solve([[0.0, 0.0], [1.0, 0.0], [10.0, 0.0]], [[0.0, 0.0], [10.0, 0.0]])
```

Output:

```text
([0, 0, 1], [[0.5, 0.0], [10.0, 0.0]])
```

**Example 2**

Input:

```python
solve([[0.0, 0.0], [1.0, 0.0]], [[0.0, 0.0], [100.0, 100.0]])
```

Output:

```text
([0, 0], [[0.5, 0.0], [100.0, 100.0]])
```

## Theory

### The simple version

K-means alternates two steps until nothing changes: (1) assign each point to its closest centre, (2) move each centre to the mean of its points. Each step can only lower the total squared distance, so the process converges, although possibly to a local optimum.

### The two steps

$$c_i=\arg\min_k\|x_i-\mu_k\|^2,\qquad \mu_k=\frac1{|C_k|}\sum_{i\in C_k}x_i$$

### Why it matters

- One k-means iteration is the whole algorithm: repeat it until nothing changes.
- Each iteration can only lower the within-cluster squared distance, so the method always converges (to a local optimum).

### How it works

1. Assign every point to its nearest centroid.
2. Move each centroid to the mean of its assigned points.
3. A centroid with no points stays where it was.

### Worked example

Points $(0,0),(1,0),(10,0)$ and centroids $(0,0),(10,0)$: the first two points are nearest to centroid 0 and the third to centroid 1, so the labels are $(0,0,1)$. Centroid 0 moves to the mean $(0.5,0)$ and centroid 1 stays at $(10,0)$: ([0, 0, 1], [[0.5, 0.0], [10.0, 0.0]]).

## Explanation

In the second example the centroid at $(100,100)$ attracts no point, so it is kept unchanged instead of becoming an undefined mean. (The previous problem sets such a centroid to zeros instead; here keeping the old position is the safer convention.)
