---
name: problem-99-pca-centering
title: 'PCA Centering'
tags: [problemset, unsupervised-ml, pca]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'pca'
hint: 'X - X.mean(axis=0)'
tools: [NumPy]
---

## Statement

Centre a data matrix feature-wise: subtract each column's mean from that column.

Implement `solve(X)`.

**Returns.** Return a float NumPy array of the same shape in which every column has mean $0$.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 10.0], [3.0, 20.0], [5.0, 30.0]])
```

Output:

```text
[[-2.0, -10.0], [0.0, 0.0], [2.0, 10.0]]
```

**Example 2**

Input:

```python
solve([[4.0, 4.0]])
```

Output:

```text
[[0.0, 0.0]]
```

## Theory

### The simple version

PCA looks for the directions in which the data varies. Variation is measured around the mean, so the mean must be removed first; otherwise the first "component" would just point at the centre of the cloud.

### The formula

$$\tilde X=X-\mathbf 1\mu^\top,\qquad \mu_j=\frac1n\sum_i X_{ij}$$

### Why it matters

- PCA measures variation around the mean, so the mean must be removed first.
- Otherwise the first component would just point at the centre of the data.

### How it works

1. Compute each column's mean.
2. Subtract it from the column.

### Worked example

The column means are $3$ and $20$. Subtracting gives $(-2,0,2)$ and $(-10,0,10)$, which as rows is [[-2.0, -10.0], [0.0, 0.0], [2.0, 10.0]].

## Explanation

Column means are computed with `axis=0` and broadcast over the rows. A single row is its own mean, so it becomes all zeros (second example). Keep the means: you need them again to reconstruct the data from its projection.
