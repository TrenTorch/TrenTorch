---
name: problem-30-correlation-matrix
title: 'Correlation Matrix'
tags: [problemset, data-stats-for-ds, eda]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-data-science|Data Processing'
topic: 'EDA'
hint: 'correlate the columns, not the rows'
tools: [NumPy]
---

## Statement

Compute the matrix of pairwise Pearson correlations between the columns of a data matrix.

Implement `solve(X)`.

**Returns.** Return a symmetric $d\times d$ NumPy array with ones on the diagonal. A constant column has no variance, so its correlations are `nan`.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 2.0], [2.0, 4.0], [3.0, 6.0]])
```

Output:

```text
[[1.0, 1.0], [1.0, 1.0]]
```

**Example 2**

Input:

```python
solve([[1.0, 3.0], [2.0, 2.0], [3.0, 1.0]])
```

Output:

```text
[[1.0, -1.0], [-1.0, 1.0]]
```

## Theory

### The simple version

Correlation measures how well two features move together on a scale from $-1$ (perfectly opposite) to $1$ (perfectly in step), regardless of units.

### The formula

$$r_{jk}=\frac{\operatorname{cov}(x_j,x_k)}{\sigma_j\,\sigma_k}$$

## Explanation

`np.corrcoef(X, rowvar=False)` treats columns as variables. A constant column has $\sigma=0$, so every correlation with it is $0/0$ and comes out as `nan`.
