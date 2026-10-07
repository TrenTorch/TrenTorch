---
name: problem-10-low-rank-reconstruction
title: 'Low-Rank Reconstruction'
tags: [problemset, maths-stats-for-ml, svd]
difficulty: Advanced
kind: problemset
relatedModule: 'part-mathematics|Linear Algebra'
topic: 'SVD'
hint: 'keep only the first k singular values, then multiply back'
tools: [NumPy]
---

## Statement

Reconstruct a matrix from only its first $k$ singular components (a truncated singular value decomposition).

Implement `solve(A, k)`.

**Returns.** Return a NumPy array of the same shape as `A`. The rank `k` is clipped into the valid range, and `k = 0` gives an all-zero matrix.

### Examples

**Example 1**

Input:

```python
solve([[3.0, 0.0], [0.0, 1.0]], 1)
```

Output:

```text
[[3.0, 0.0], [0.0, 0.0]]
```

**Example 2**

Input:

```python
solve([[1.0, 2.0], [3.0, 4.0]], 2)
```

Output:

```text
[[1.0, 2.0], [3.0, 4.0]]
```

## Theory

### The simple version

An SVD writes a matrix as a sum of simple rank-one pieces, ordered from most to least important. Keeping only the biggest $k$ pieces gives the best possible rank-$k$ approximation of the original.

### The formula

$$A_k=\sum_{i=1}^{k}\sigma_i\,u_i v_i^\top,\qquad \|A-A_k\|_F^2=\sum_{i>k}\sigma_i^2$$

The second identity is the Eckart-Young theorem.

## Explanation

The reference computes a thin SVD, keeps the first $k$ singular values and vectors, and multiplies them back together. Using $k$ equal to the rank returns the original matrix up to rounding.
