---
name: problem-6-frobenius-norm
title: 'Frobenius Norm'
tags: [problemset, maths-stats-for-ml, linear-algebra]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Linear Algebra'
topic: 'linear algebra'
hint: 'sum squared entries before taking one square root'
tools: [NumPy]
---

## Statement

Implement `solve(A)`. Compute the Frobenius norm of a non-empty matrix.

### Examples

**Example 1**

Input:

```python
solve([[3.0, 4.0], [0.0, 12.0]])
```

Output:

```text
13.0
```

**Example 2**

Input:

```python
solve([[1.0, 2.0]])
```

Output:

```text
2.23606797749979
```

## Theory

The Frobenius norm is the square root of the sum of squares of all matrix entries.

## Explanation

Convert the inputs to numeric arrays where appropriate, apply the stated operation, and return its result without printing. The examples show the required argument order and output form.
