---
name: numpy-solving-linear-systems
title: np.linalg.solve
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement a function solving a system of linear equations using `np.linalg.solve`, and understand why this is preferred over explicitly computing a matrix inverse.

## Theory

A system $Ax = b$ can be solved directly:

```python
A = np.array([[2, 1], [1, -1]])
b = np.array([5, 1])
x = np.linalg.solve(A, b)     # [2., 1.]
```

One alternative is $x = A^{-1}b$, but this is **not preferred**: computing a full inverse is more expensive, and explicitly forming it tends to accumulate more floating-point error than solving directly — especially for larger or less well-behaved matrices.

```python
x_via_inverse = np.linalg.inv(A) @ b     # equivalent, but not preferred
x_via_solve = np.linalg.solve(A, b)        # preferred
```

`np.linalg.solve` requires $A$ to be square and invertible, raising an error for a singular coefficient matrix.

## Explanation

`solve_system` is `np.linalg.solve(coefficients, constants)`. `solve_via_inverse` is `np.linalg.inv(coefficients) @ constants`, existing purely for comparison. `solutions_agree` computes both and checks `np.allclose` between them.
