---
name: numpy-inverse-and-determinant
title: np.linalg.inv and np.linalg.det
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions computing a matrix's determinant and inverse, and verify the defining relationship between a matrix and its inverse directly.

## Theory

**The determinant**, `np.linalg.det`, captures whether a square matrix has an inverse: a matrix has an inverse iff its determinant is **not zero**. A matrix with determinant exactly zero is **singular**, with no inverse.

```python
A = np.array([[1, 2], [3, 4]])
np.linalg.det(A)     # 1*4 - 2*3 = -2.0

singular = np.array([[1, 2], [2, 4]])
np.linalg.det(singular)     # 0.0
```

**The inverse** $A^{-1}$ satisfies $A \cdot A^{-1} = A^{-1} \cdot A = I$ (the identity matrix, `np.eye(n)`).

```python
A_inv = np.linalg.inv(A)
A @ A_inv     # approximately the identity matrix
```

`np.linalg.inv` raises an error on a singular matrix.

## Explanation

`determinant` calls `np.linalg.det(matrix)`. `is_invertible` checks `abs(determinant(matrix)) > 1e-10` rather than exact equality to zero, since floating-point computation rarely yields an exact `0.0`. `safe_inverse` checks `is_invertible` first, returning `np.linalg.inv(matrix)` if true or `None` otherwise — never letting the error propagate. `verify_inverse` checks `np.allclose(matrix @ inverse, np.eye(len(matrix)))`.
