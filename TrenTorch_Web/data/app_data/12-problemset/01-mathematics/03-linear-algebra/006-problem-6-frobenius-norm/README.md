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

### Why it matters

- The Frobenius norm is the natural size of a matrix: the length of the matrix treated as one long vector.
- It is used in weight decay and in measuring how well one matrix approximates another.

### How it works

1. Square every entry.
2. Add all the squares.
3. Take the square root.

### Worked example

For the single row $(3,4)$ the squares are $9$ and $16$, they add to $25$, and the square root is 5.0.

## Explanation

`np.linalg.norm(A, ord="fro")` sums the squares of every entry and takes the square root. The trace identity shows it also equals the square root of the sum of the diagonal of the Gram matrix.
