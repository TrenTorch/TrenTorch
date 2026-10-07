---
name: problem-8-solve-a-2-2-linear-system
title: 'Solve a 2×2 Linear System'
tags: [problemset, maths-stats-for-ml, linear-algebra]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Linear Algebra'
topic: 'linear algebra'
hint: 'Cramer’s rule, and guard a zero determinant'
tools: [NumPy]
---

## Statement

Solve the system $ax+by=e$, $cx+dy=f$ for $x$ and $y$ without calling a linear solver. The six numbers arrive as the list `[a, b, c, d, e, f]`.

Implement `solve(coeffs)`.

**Returns.** Return `[x, y]` as a NumPy array. A singular system (determinant $0$) has no unique solution and raises `ValueError`.

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
solve([1, 2, 2, 4, 3, 6])
```

Output: Raises `ValueError`.

## Theory

### The simple version

Two straight lines usually cross at exactly one point, and that point is the solution. Cramer's rule finds it with determinants.

### The formula

$$x=\frac{ed-bf}{ad-bc},\qquad y=\frac{af-ec}{ad-bc}$$

The denominator $ad-bc$ is the determinant of the coefficient matrix.

## Explanation

A zero determinant means the lines are parallel or identical, so there is no single crossing point and dividing would be meaningless. The function raises `ValueError` in that case instead of returning infinities.
