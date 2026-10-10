---
name: problem-94-complete-link-distance
title: 'Complete-Link Distance'
tags: [problemset, unsupervised-ml, hierarchical-clustering]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'hierarchical clustering'
hint: 'maximum over all pairwise Euclidean distances'
tools: [NumPy]
---

## Statement

Compute the complete-link distance between two clusters: the largest Euclidean distance between a point of the first cluster and a point of the second.

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
2.236068
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

Complete link measures two groups by their _furthest_ pair of members, so two clusters are only considered close if every point of one is fairly near every point of the other. It produces compact, similar-sized clusters.

### The formula

$$d_{\text{complete}}(A,B)=\max_{a\in A,\,b\in B}\|a-b\|_2$$

### Why it matters

- Complete link uses the farthest pair, so merged clusters stay compact.
- It is less prone to chaining than single link.

### How it works

1. Compute all pairwise distances between the two clusters.
2. Take the maximum.

### Worked example

Using the same four distances $1$, $2.236$, $1.414$, $1.414$, the largest is 2.236068.

## Explanation

It is the same pairwise-distance matrix as for single link but with a maximum instead of a minimum. For the same inputs complete link is always at least as large as single link.
