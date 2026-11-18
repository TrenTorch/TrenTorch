---
name: problem-7-gram-matrix
title: 'Gram Matrix'
tags: [problemset, maths-stats-for-ml, linear-algebra]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Linear Algebra'
topic: 'linear algebra'
hint: 'transpose X and multiply'
tools: [NumPy]
---

## Statement

Given a data matrix $X$ whose rows are samples and whose columns are features, compute the Gram matrix $X^\top X$ of its columns.

Implement `solve(X)`.

**Returns.** Return a symmetric NumPy array of shape $(d, d)$ for $d$ columns.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 2.0], [3.0, 4.0]])
```

Output:

```text
[[10.0, 14.0], [14.0, 20.0]]
```

**Example 2**

Input:

```python
solve([[1.0, 0.0], [0.0, 1.0]])
```

Output:

```text
[[1.0, 0.0], [0.0, 1.0]]
```

## Theory

### The simple version

Entry $(j, k)$ of the Gram matrix is the dot product of column $j$ with column $k$, so it records how strongly each pair of features line up across the samples.

### The formula

$$G_{jk}=\sum_i X_{ij}X_{ik},\qquad G=X^\top X$$

$G$ is always symmetric and positive semi-definite.

### Why it matters

- The Gram matrix collects the inner products between all pairs of features, so it summarises how features relate to each other.
- It is the core of least squares ($X^\top X$), kernels and covariance estimates, and it is always symmetric and positive semi-definite.

### How it works

1. Take the columns of $X$ as vectors.
2. Entry $(i,j)$ is the dot product of column $i$ with column $j$.
3. Equivalently, compute $X^\top X$ in one matrix product.

### Worked example

For the matrix with columns $(1,3)$ and $(2,4)$: $(1,3)\cdot(1,3)=10$, $(1,3)\cdot(2,4)=14$ and $(2,4)\cdot(2,4)=20$, which gives [[10.0, 14.0], [14.0, 20.0]].

## Explanation

One matrix product computes every pairwise column dot product at once. The result has one row and column per feature, regardless of how many samples there are.
