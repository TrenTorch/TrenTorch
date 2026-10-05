---
name: problem-14-hessian-diagonal
title: 'Hessian Diagonal'
tags: [problemset, maths-stats-for-ml, calculus]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Calculus'
topic: 'calculus'
hint: 'use the centered second-difference formula'
tools: [NumPy]
---

## Statement

Implement `solve(f, x, h=1e-5)`. Approximate the diagonal of the Hessian of a scalar-valued function at vector x with centered second differences.

### Examples

**Example 1**

Input:

```python
solve(lambda z: np.sum(z*z), [1.0, 2.0])
```

Output:

```text
[2.0000001654807416, 2.0000001654807416]
```

**Example 2**

Input:

```python
solve(lambda z: z[0]**2 + 3*z[1]**2, [0.0, 1.0])
```

Output:

```text
[2.0000001654807416, 6.000009378226422]
```

## Theory

The second derivative along each coordinate uses [f(x+h eᵢ)-2f(x)+f(x-h eᵢ)]/h²; mixed partials are not computed.

## Explanation

Convert the inputs to numeric arrays where appropriate, apply the stated operation, and return its result without printing. The examples show the required argument order and output form.
