---
name: center-features-for-pca-company-212
title: 'center-features-for-pca — Apple case'
tags: [problemset, unsupervised-ml, pca, apple]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'Classic ML'
caseCompany: 'Apple'
hint: 'X - X.mean(axis=0)'
tools: [NumPy]
---

## Statement

Apple-inspired on-device analytics pipeline is preparing correlated sensor features for dimensionality reduction. The team needs each feature centered before PCA, and you need to compute that centered matrix without changing the original observations beyond subtracting their means.

Subtract each column's mean from that column. Nothing else about the data changes.

Implement `solve(X)`.

**Returns.** Return a float NumPy matrix of the same shape in which every column has mean $0$.

Subtract each column's mean from that column. Nothing else about the data changes.

Implement `solve(X)`.

**Returns.** Return a float NumPy matrix of the same shape in which every column has mean $0$.

### Examples

**Example 1**

Input:

```python
solve([[1, 2], [3, 4]])
```

Output:

```text
[[-1.0, -1.0], [1.0, 1.0]]
```

**Example 2**

Input:

```python
solve([[2.0, 5.0], [4.0, 5.0], [6.0, 5.0]])
```

Output:

```text
[[-2.0, 0.0], [0.0, 0.0], [2.0, 0.0]]
```

## Theory

### The simple version

PCA finds the directions along which the data varies most. Variation is measured around the mean, so the data must be centred first; otherwise the first component would point at the centre of the cloud instead of along its spread.

### The formula

$$\tilde X=X-\mathbf 1\mu^\top,\qquad \mu_j=\frac1n\sum_iX_{ij}$$

### Why it matters

- PCA measures variation around the mean, so the data must be centred first.
- Otherwise the first component would point at the middle of the data cloud instead of along its spread.

### How it works

1. Compute each column's mean.
2. Subtract it from the column.

### Worked example

The column means are $2$ and $3$. Subtracting gives $(1-2,\,2-3)=(-1,-1)$ and $(3-2,\,4-3)=(1,1)$: [[-1.0, -1.0], [1.0, 1.0]].

## Explanation

The means are computed per column (`axis=0`) and broadcast over the rows. A constant column (second example) becomes all zeros: it has no variation to explain.
