---
name: research-double-descent-ridge
title: 'Deep Double Descent: The Ridge Solution'
tags: [research-papers, classical-ml, learning-theory, double-descent]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Ridge regression adds an L2 penalty, which makes the normal equations solvable even when there are more features than samples. As the penalty goes to zero, ridge approaches the minimum-norm solution, linking it back to double descent.

### From theory to code

Implement `ridge_solution(X, y, lam)`, returning `(X^T X + lam I)^{-1} X^T y`.

### Constraints

- Use `np.linalg.solve`; do not form an inverse explicitly.

### Hints

<details>
<summary>Hint 1</summary>

Build the regularized Gram matrix and the right-hand side, then solve.

</details>

## Theory

### The simple version

The penalty shifts every eigenvalue of `X^T X` up by `lam`, so the matrix is invertible and small directions of the data get shrunk the most.

### The formula

$$w_\lambda = (X^\top X + \lambda I)^{-1} X^\top y$$

### How NumPy/PyTorch actually implements this

`sklearn.linear_model.Ridge` solves this system, usually with a Cholesky factorization.

## Explanation

As lambda goes to zero this converges to the least-squares solution when `X^T X` is invertible, and to the minimum-norm solution in the overparameterized case.
