---
name: problem-5-matrix-transpose
title: "Matrix Transpose"
tags: [problemset, maths-stats-for-ml, linear-algebra]
difficulty: Intermediate
kind: problemset
relatedModule: "part-math|Linear Algebra"
topic: "linear algebra"
hint: "swap row and column indices"
tools: [NumPy]
---

# Matrix Transpose

## Statement

Implement `solve(A)`. Return the transpose of a rectangular matrix, exchanging its row and column axes.

## Theory

Transposition maps entry A[i, j] to Aᵀ[j, i].

## Explanation

Convert the inputs to numeric arrays where appropriate, apply the stated operation, and return its result without printing. The examples show the required argument order and output form.

## Examples

**Example 1**

Input:
```python
solve([[1, 2, 3], [4, 5, 6]])
```

Output:
```text
[[1, 4], [2, 5], [3, 6]]
```

**Example 2**

Input:
```python
solve([[7, 8]])
```

Output:
```text
[[7], [8]]
```
