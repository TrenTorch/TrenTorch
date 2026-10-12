---
name: problem-95-dbscan-core-point
title: 'DBSCAN Core Point'
tags: [problemset, unsupervised-ml, dbscan]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'dbscan'
hint: 'count points with squared distance <= eps^2 (itself included) and compare with min_samples'
tools: [NumPy]
---

## Statement

Decide whether point `i` is a DBSCAN core point: it is a core point if at least `min_samples` points (**including itself**) lie within Euclidean distance `eps` of it.

Implement `solve(X,i,eps,min_samples=1)`.

**Returns.** Return `1` if point `i` is a core point and `0` otherwise.

### Examples

**Example 1**

Input:

```python
solve([[0.0, 0.0], [0.1, 0.0], [3.0, 3.0]], 0, 0.2, 2)
```

Output:

```text
1
```

**Example 2**

Input:

```python
solve([[0.0, 0.0], [0.1, 0.0], [3.0, 3.0]], 2, 0.2, 2)
```

Output:

```text
0
```

## Theory

### The simple version

DBSCAN grows clusters outward from dense places. A point is _dense_ (a core point) if its $\varepsilon$-neighbourhood contains enough points. Core points seed and extend clusters; points near a core point join as border points; the rest are noise.

### The rule

$$\text{core}(p)\iff\big|\{q:\|q-p\|\le\varepsilon\}\big|\ge\text{min\_samples}$$

### Why it matters

- DBSCAN grows clusters from dense points, so identifying a core point is the first step.
- Sparse points become noise instead of being forced into a cluster.

### How it works

1. Find all points within distance $\varepsilon$ of the point (including itself).
2. It is a core point if their number is at least `min_samples`.

### Worked example

Around point $0=(0,0)$ with $\varepsilon=0.2$ lie itself and $(0.1,0)$, two points. With `min_samples=2` that is enough, so the result is 1 (core).

## Explanation

The neighbourhood count includes the point itself (its distance to itself is $0\le\varepsilon$), which matches scikit-learn's convention. In the first example point 0 and point 1 are within $0.2$ of each other, giving a count of $2$; point 2 is isolated with a count of $1$.
