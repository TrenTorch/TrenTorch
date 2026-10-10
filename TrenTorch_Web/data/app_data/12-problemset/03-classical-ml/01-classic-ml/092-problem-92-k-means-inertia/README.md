---
name: problem-92-k-means-inertia
title: 'K-Means Inertia'
tags: [problemset, unsupervised-ml, clustering-evaluation]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'clustering evaluation'
hint: 'sum of squared distances from each point to its assigned centroid'
tools: [NumPy]
---

## Statement

Compute the k-means inertia: the total squared Euclidean distance between each point and the centroid of the cluster it is assigned to.

Implement `solve(X,C,labels)`.

**Returns.** Return a non-negative float. `labels[i]` is the index of the centroid assigned to `X[i]`.

### Examples

**Example 1**

Input:

```python
solve([[0.0, 0.0], [2.0, 0.0], [10.0, 10.0]], [[1.0, 0.0], [10.0, 10.0]], [0, 0, 1])
```

Output:

```text
2.0
```

**Example 2**

Input:

```python
solve([[1.0, 1.0]], [[1.0, 1.0]], [0])
```

Output:

```text
0.0
```

## Theory

### The simple version

Inertia is the objective k-means is trying to minimise: how far, in total, the points are from their cluster centres (squared). A smaller value means tighter clusters, but it always falls as $K$ grows, so you cannot simply pick the $K$ with the smallest inertia.

### The formula

$$J=\sum_{k}\sum_{i\in C_k}\|x_i-\mu_k\|^2$$

### Why it matters

- Inertia is the quantity k-means minimises, so it is the natural score for a clustering.
- Plotting it against $K$ (the elbow method) helps choose the number of clusters.

### How it works

1. For each point take the squared distance to its assigned centroid.
2. Add them all up.

### Worked example

Cluster 0 has centroid $(1,0)$ and points $(0,0)$ and $(2,0)$, each at squared distance $1$. Cluster 1 has centroid $(10,10)$ and its single point sits on it (distance $0$). The total is $1+1+0=2.0$.

## Explanation

For each centroid the squared distances of its own points are added up. In the first example the two points of cluster 0 are each at distance $1$ from $(1,0)$ and cluster 1 sits exactly on its centre, so the inertia is $1+1+0=2$. Plotting inertia against $K$ and looking for the bend is the "elbow method".
