---
name: problem-104-silhouette-score-one-point
title: 'Silhouette Score One Point'
tags: [problemset, unsupervised-ml, clustering-metrics]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'clustering metrics'
hint: 'a = mean(intra), b = min(nearest), s = (b - a) / max(a, b)'
tools: [NumPy]
---

## Statement

Compute the silhouette score of a single point. `intra` holds the distances from the point to the other members of its own cluster, and `nearest` holds the average distances from the point to each of the other clusters. With $a$ = mean of `intra` and $b$ = smallest value in `nearest`, the score is $(b-a)/\max(a,b)$, or $0$ when both are zero.

Implement `solve(intra, nearest)`.

**Returns.** Return a float in $[-1,1]$. `intra` and `nearest` must not be empty.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0], [5.0, 7.0])
```

Output:

```text
0.7
```

**Example 2**

Input:

```python
solve([4.0], [2.0])
```

Output:

```text
-0.5
```

**Example 3**

Input:

```python
solve([0.0], [0.0])
```

Output:

```text
0.0
```

## Theory

### The simple version

The silhouette asks of one point: am I closer to my own cluster than to the next nearest one? A value near $+1$ means well placed, near $0$ means on the border between two clusters, and negative means probably assigned to the wrong cluster.

### The formula

$$s=\frac{b-a}{\max(a,b)}$$

where $a$ is the mean distance to the point's own cluster and $b$ is the mean distance to the nearest other cluster.

### Why it matters

- The silhouette measures how well a point fits its cluster compared with the nearest other cluster.
- Averaged over points it scores a whole clustering.

### How it works

1. $a$ = mean distance to the point's own cluster.
2. $b$ = smallest mean distance to another cluster.
3. $s=(b-a)/\max(a,b)$.

### Worked example

Distances to its own cluster $(1,2)$ give $a=1.5$, and the nearest other cluster is at $b=5$. So $s=(5-1.5)/5=0.7$.

## Explanation

In the first example $a=1.5$ and $b=5$, so $s=(5-1.5)/5=0.7$, a confident assignment. In the second the point is farther from its own cluster ($4$) than from the neighbour ($2$), giving $-0.5$. If every distance is zero the ratio is $0/0$, and `0.0` is returned.
