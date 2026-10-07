---
name: problem-6-frobenius-norm
title: 'Frobenius Norm'
tags: [problemset, maths-stats-for-ml, linear-algebra]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Linear Algebra'
topic: 'linear algebra'
hint: 'square every entry, add, take the square root'
tools: [NumPy]
---

## Statement

Compute the Frobenius norm of a matrix: the square root of the sum of the squares of all its entries.

Implement `solve(A)`.

**Returns.** Return a float.

### Examples

**Example 1**

Input:

```python
solve([[3.0, 4.0]])
```

Output:

```text
5.0
```

**Example 2**

Input:

```python
solve([[1.0, 2.0], [2.0, 4.0]])
```

Output:

```text
5.0
```

## Theory

### The simple version

The Frobenius norm treats the matrix as one long vector and takes its ordinary L2 norm. It measures the overall size of the matrix.

### The formula

$$\|A\|_F=\sqrt{\sum_{i,j}A_{ij}^2}=\sqrt{\operatorname{tr}(A^\top A)}$$

## Explanation

`np.linalg.norm(A, ord="fro")` sums the squares of every entry and takes the square root. The trace identity shows it also equals the square root of the sum of the diagonal of the Gram matrix.
