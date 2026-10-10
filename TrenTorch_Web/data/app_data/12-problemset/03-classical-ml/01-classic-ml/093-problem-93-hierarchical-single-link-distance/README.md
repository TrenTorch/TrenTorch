---
name: problem-93-hierarchical-single-link-distance
title: 'Hierarchical Single-Link Distance'
tags: [problemset, unsupervised-ml, hierarchical-clustering]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'hierarchical clustering'
hint: 'minimum over all pairwise Euclidean distances'
tools: [NumPy]
---

## Statement

Compute the single-link distance between two clusters: the smallest Euclidean distance between a point of the first cluster and a point of the second.

Implement `solve(A,B)`.

**Returns.** Return a non-negative float. `A` and `B` are arrays of points with the same number of coordinates.

### Examples

**Example 1**

Input:

```python
solve([[0.0, 0.0], [1.0, 0.0]], [[0.0, 1.0], [2.0, 1.0]])
```

Output:

```text
1.0
```

**Example 2**

Input:

```python
solve([[0.0, 0.0]], [[3.0, 4.0]])
```

Output:

```text
5.0
```

## Theory

### The simple version

Hierarchical clustering needs a way to say how far apart two _groups_ of points are. Single link says: as far apart as their two closest members. It tends to chain clusters together through thin bridges of points.

### The formula

$$d_{\text{single}}(A,B)=\min_{a\in A,\,b\in B}\|a-b\|_2$$

### Why it matters

- Agglomerative clustering must decide how far apart two groups are.
- Single link uses the closest pair, which lets clusters chain together through thin bridges.

### How it works

1. Compute the distance between every point of $A$ and every point of $B$.
2. Take the minimum.

### Worked example

The four pairwise distances between $\{(0,0),(1,0)\}$ and $\{(0,1),(2,1)\}$ are $1$, $\sqrt5=2.236$, $\sqrt2=1.414$ and $\sqrt2=1.414$. The smallest is 1.0.

## Explanation

Broadcasting computes all $|A|\cdot|B|$ pairwise distances at once and the minimum is taken. In the second example the two single points are $5$ apart (a 3-4-5 triangle).
