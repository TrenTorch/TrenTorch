---
name: math-negative-definite-matrices
title: Negative Definite & Semi-Definite Matrices
tags: [linear-algebra, matrices, optimization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A bowl has a lowest point. Turn it upside down and it has a highest point, a hilltop where every direction curves down. The matrices that describe an upside-down bowl are the mirror image of the ones in `01-positive-definite` and `02-positive-semidefinite`: the quadratic form is negative in every direction, or at worst zero along some of them. Maximizing a smooth function, as in maximum-likelihood estimation or a reward objective, is exactly the problem of finding such a hilltop. This question builds the two tests and uses them to find the peak of a quadratic function, which exists and is unique only when the curvature has this shape.

### From theory to code

Implement `is_negative_definite(a)` and `is_negative_semidefinite(a, tol)`, then `quadratic_maximizer(a, b)`, which returns the single highest point of `f(x) = 0.5 * x^T a x + b^T x` when one exists. The signatures and docstrings are already in the editor.

### Constraints

- Both tests require a square, symmetric matrix (within `np.allclose`). A non-symmetric matrix is neither.
- `is_negative_definite` uses a strict test: every eigenvalue is strictly below zero. `is_negative_semidefinite` allows eigenvalues up to `tol`, so an eigenvalue of `1e-12` counts as zero while `1e-3` does not, with the default `tol = 1e-10`.
- `quadratic_maximizer(a, b)` takes a square symmetric `a` and a 1D `b` of matching length. It raises `ValueError` unless `a` is negative definite, because otherwise the function has no unique highest point.
- Inputs must not be modified.

### Hints

<details>
<summary>Hint 1</summary>

Flipping every sign of a matrix flips every sign of its quadratic form, so `a` is negative definite exactly when `-a` is positive definite. Both tests are the earlier tests applied to `-a`.

</details>

<details>
<summary>Hint 2</summary>

The highest point is where the gradient `a x + b` is zero. Solve that linear system rather than inverting the matrix.

</details>

## Theory

### The simple version

Hold the bowl from `01-positive-definite` upside down. A ball placed anywhere on it rolls off in every direction, but there is exactly one point where it can balance, the top. That balance point exists and is unique because every direction curves downward. If some direction were flat the ball could rest anywhere along it, and if some direction curved upward there would be no top at all.

### The formulas

A symmetric matrix $A$ is **negative definite** if

$$
x^{\top} A x < 0 \quad \text{for all } x \neq 0
$$

and **negative semi-definite** if $x^{\top} A x \le 0$ for all $x$.

- Negating a matrix negates its quadratic form, so $A$ is negative definite exactly when $-A$ is positive definite, and negative semi-definite exactly when $-A$ is positive semi-definite.
- In eigenvalue terms, negative definite means every eigenvalue is strictly negative, and negative semi-definite means every eigenvalue is $\le 0$. A negative semi-definite matrix with a zero eigenvalue is singular.
- A matrix cannot be both positive and negative definite. The only matrix that is both positive and negative **semi**-definite is the zero matrix.

### The peak of a quadratic function

The function $f(x) = \tfrac{1}{2} x^{\top} A x + b^{\top} x$ has gradient $Ax + b$. Setting it to zero gives the stationary point

$$
x^{*} = -A^{-1} b
$$

When $A$ is negative definite this point is the unique global maximum, with value

$$
f(x^{*}) = -\tfrac{1}{2}\, b^{\top} A^{-1} b
$$

since the function curves down away from $x^{*}$ in every direction. When $A$ is only negative semi-definite there is either no stationary point or a whole flat line of them, and when $A$ has a positive eigenvalue the stationary point is a saddle.

### Where this shows up in machine learning

A log-likelihood that is concave has a negative semi-definite Hessian everywhere, which is why logistic regression has a single optimum that any ascent method finds. The Hessian of a loss at a local maximum is negative definite, and checking this is how second-order methods tell a peak from a saddle. Gaussian log-densities are exactly quadratic functions of this type, with $A$ equal to minus the precision matrix.

### How NumPy/PyTorch actually implements this

`np.linalg.eigvalsh(-a)` tests negative definiteness through the eigenvalues of the negated matrix, and `np.linalg.solve(a, -b)` returns the stationary point without forming the inverse. `torch.linalg.solve` does the same on tensors, and in practice an optimizer walks to the top by following the gradient instead of solving for it directly.

## Explanation

`is_negative_definite` requires a square symmetric matrix and then checks that the largest eigenvalue, the last entry of `np.linalg.eigvalsh`, is strictly below zero, which is the same as every eigenvalue being negative. `is_negative_semidefinite` does the same with the largest eigenvalue allowed up to `tol`. `quadratic_maximizer` raises `ValueError` unless `is_negative_definite(a)` holds, since only then is there a unique highest point, and otherwise returns `np.linalg.solve(a, -b)`, the zero of the gradient `a x + b`, which avoids forming the inverse.
