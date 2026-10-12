---
name: problem-100-pca-covariance
title: 'PCA Covariance'
tags: [problemset, unsupervised-ml, pca]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'pca'
hint: 'centre X, then Z.T @ Z / (n - 1)'
tools: [NumPy]
---

## Statement

Compute the sample covariance matrix of a data matrix `X` with $n$ rows (samples) and $d$ columns (features), dividing by $n-1$.

Implement `solve(X)`.

**Returns.** Return a symmetric $d\times d$ float NumPy array. At least two rows are needed; a single row has no sample covariance (the result is `nan`).

### Examples

**Example 1**

Input:

```python
solve([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
```

Output:

```text
[[4.0, 4.0], [4.0, 4.0]]
```

**Example 2**

Input:

```python
solve([[1.0, 0.0], [2.0, 0.0], [3.0, 0.0]])
```

Output:

```text
[[1.0, 0.0], [0.0, 0.0]]
```

## Theory

### The simple version

The covariance matrix records how every pair of features moves together. Its diagonal holds each feature's variance and the off-diagonal entries hold the covariances. PCA is the eigen-decomposition of this matrix.

### The formula

$$S=\frac1{n-1}\,\tilde X^\top\tilde X,\qquad \tilde X=X-\bar X$$

### Why it matters

- The covariance matrix is what PCA diagonalises.
- Its entries show which features vary together.

### How it works

1. Centre the data.
2. Compute $\tilde X^\top\tilde X$.
3. Divide by $n-1$.

### Worked example

The columns $(1,3,5)$ and $(2,4,6)$ have the same spread: centred values $(-2,0,2)$ for both, so every entry is $(4+0+4)/2=4$, giving [[4.0, 4.0], [4.0, 4.0]].

## Explanation

The data are centred first, then $\tilde X^\top\tilde X$ collects all pairwise products at once. Dividing by $n-1$ (Bessel's correction) makes the estimate unbiased. A constant feature (second example) has zero variance and zero covariance with everything.
