---
name: problem-7-gram-matrix
title: 'Gram Matrix'
tags: [problemset, maths-stats-for-ml, linear-algebra]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Linear Algebra'
topic: 'linear algebra'
hint: 'accumulate feature-feature products'
tools: [NumPy]
---

## Statement

Implement `solve(X)`. Compute the Gram matrix XᵀX of a two-dimensional data matrix X.

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
solve([[1.0], [2.0], [3.0]])
```

Output:

```text
[[14.0]]
```

## Theory

The (i,j) entry is the dot product of feature columns i and j, so the result is symmetric and positive semidefinite.

## Explanation

Convert the inputs to numeric arrays where appropriate, apply the stated operation, and return its result without printing. The examples show the required argument order and output form.
