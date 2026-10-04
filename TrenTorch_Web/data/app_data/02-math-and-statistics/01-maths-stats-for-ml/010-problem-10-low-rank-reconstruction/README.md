---
name: problem-10-low-rank-reconstruction
title: "Low-Rank Reconstruction"
tags: [problemset, maths-stats-for-ml, svd]
difficulty: Advanced
kind: problemset
relatedModule: "part-math|Linear Algebra"
topic: "SVD"
hint: "multiply U[:,:k], diag(S[:k]), and Vt[:k,:]"
tools: [NumPy]
---

# Low-Rank Reconstruction

## Statement

Implement `solve(A, k)`. Reconstruct A from its first k singular components using a truncated singular value decomposition.

## Theory

The best rank-k approximation in Frobenius norm is formed by keeping the k largest singular values and corresponding singular vectors.

## Explanation

Convert the inputs to numeric arrays where appropriate, apply the stated operation, and return its result without printing. The examples show the required argument order and output form.

## Examples

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
[[1.0000000000000009, 2.0], [3.000000000000001, 4.0]]
```
