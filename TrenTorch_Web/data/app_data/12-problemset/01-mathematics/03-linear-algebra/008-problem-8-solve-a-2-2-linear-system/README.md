---
name: problem-8-solve-a-2-2-linear-system
title: 'Solve a 2×2 Linear System'
tags: [problemset, maths-stats-for-ml, linear-algebra]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Linear Algebra'
topic: 'linear algebra'
hint: 'use the closed-form determinant and handle a zero determinant'
tools: [NumPy]
---

## Statement

Implement `solve(coeffs)`. Solve the system a*x + b*y = e and c*x + d*y = f, where coeffs is [a,b,c,d,e,f]. A singular system raises ValueError.

### Examples

**Example 1**

Input:

```python
solve([2, 1, 1, 3, 5, 7])
```

Output:

```text
[1.6, 1.8]
```

**Example 2**

Input:

```python
solve([1, 0, 0, 1, -2, 4])
```

Output:

```text
[-2.0, 4.0]
```

## Theory

Cramer’s rule gives each unknown as a determinant ratio; the determinant of the coefficient matrix must be nonzero.

## Explanation

Convert the inputs to numeric arrays where appropriate, apply the stated operation, and return its result without printing. The examples show the required argument order and output form.
