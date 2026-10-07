---
name: dbscan-core-point-company-234
title: 'dbscan-core-point — Ola case'
tags: [problemset, unsupervised-ml, dbscan, ola]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'Classic ML'
caseCompany: 'Ola'
hint: 'pairwise distances <= eps, count per row, compare with min_samples'
tools: [NumPy]
---

## Statement

Ola-inspired location-clustering service must identify dense groups of nearby pickup points while treating sparse points differently. You need to determine whether each point is a DBSCAN core point under the supplied radius and minimum-neighbor rules.

For every point, decide whether it is a DBSCAN **core point**: it is one if at least `min_samples` points (itself included) lie within Euclidean distance `eps` of it, boundary included.

Implement `solve(X,eps,min_samples)`.

**Returns.** Return a boolean NumPy array with one entry per point.

### Examples

**Example 1**

Input:

```python
solve([[0, 0], [0, 1], [5, 5]], 1.1, 2)
```

Output:

```text
[True, True, False]
```

**Example 2**

Input:

```python
solve([[0.0], [1.0], [2.0], [3.0]], 1.0, 3)
```

Output:

```text
[False, True, True, False]
```

## Theory

### The simple version

DBSCAN looks for dense regions. A core point sits in such a region: enough other points live within a small radius of it. Clusters grow outward from core points; points that are close to a core point but not dense themselves become border points; the rest are noise.

### The rule

$$\text{core}(p)\iff\#\{q:\|p-q\|\le\varepsilon\}\ge\text{min\_samples}$$

## Explanation

The count includes the point itself (its distance to itself is $0$). In the first example the first two points are within $1.1$ of each other, so each has 2 neighbours counting itself; the isolated third point only has itself. In the second example the two middle points have three neighbours each.
