---
name: problem-96-dbscan-region-query
title: 'DBSCAN Region Query'
tags: [problemset, unsupervised-ml, dbscan]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'dbscan'
hint: 'indices where squared distance to X[i] is <= eps^2'
tools: [NumPy]
---

## Statement

Find the DBSCAN $\varepsilon$-neighbourhood of a point: the indices of all points (including the point itself) whose Euclidean distance to point `i` is at most `eps`.

Implement `solve(X,i,eps)`.

**Returns.** Return an integer NumPy array of indices in increasing order.

### Examples

**Example 1**

Input:

```python
solve([[0.0, 0.0], [0.1, 0.0], [3.0, 3.0]], 0, 0.2)
```

Output:

```text
[0, 1]
```

**Example 2**

Input:

```python
solve([[0.0], [1.0], [2.0], [3.0]], 1, 1.0)
```

Output:

```text
[0, 1, 2]
```

## Theory

### The simple version

A region query answers "who lives near this point?". DBSCAN runs it once per point; the size of the answer decides whether the point is dense enough to start or grow a cluster.

### The definition

$$N_\varepsilon(p)=\{\,q:\|q-p\|_2\le\varepsilon\,\}$$

### Why it matters

- The region query is the neighbourhood lookup DBSCAN performs for every point.
- Its result decides density and which points join a cluster.

### How it works

1. Compute squared distances from point $i$ to all points.
2. Keep the indices with distance at most $\varepsilon^2$.

### Worked example

Point $0=(0,0)$ with $\varepsilon=0.2$: itself (distance $0$), $(0.1,0)$ (distance $0.1$) and $(3,3)$ (distance $4.24$). Only the first two qualify: [0, 1].

## Explanation

Squared distances are compared with $\varepsilon^2$ so no square root is needed. The boundary is inclusive (`<=`), and point `i` is always in its own neighbourhood because its distance to itself is $0$. In the second example the neighbours of point 1 at distance exactly $1$ are included.
