---
name: math-positive-definite-matrices
title: 'Positive-definite matrices, and why they matter for optimization'
tags: [linear-algebra, matrices, optimization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Stand at the bottom of a bowl and every direction you step curves back up, you're at a minimum. Stand on a mountain pass and some directions curve up, others curve down, a saddle. Stand at the top of a hill and every direction curves down, a maximum. A single matrix, the Hessian (second derivatives, the next question in this track), tells you which of these three situations you're actually in at any point where a function's slope is zero, and "positive-definite" is the precise, checkable condition for "every direction curves up", i.e. a genuine minimum.

This matters concretely: every training loop in this curriculum stops when the gradient is (near) zero, but zero gradient alone doesn't tell you whether you've found a good minimum, a bad maximum, or a saddle point stalling training. Positive-definiteness is the test that distinguishes them.

### From theory to code

Theory defines positive-definiteness via a quadratic form (`x^T A x > 0` for every nonzero `x`) that's impossible to check exhaustively, and gives an equivalent, checkable condition instead: symmetric, with every eigenvalue strictly positive. Implement the quadratic form directly (so you can see the definition compute a real number), then the checkable eigenvalue-based test.

Implement `is_symmetric(a)`, `quadratic_form(a, x)` and `is_positive_definite(a)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- Positive-definiteness is only checked for square matrices, and requires symmetry first.
- Use strict `> 0` on eigenvalues, not `>= 0` (that weaker condition is a different, related property, positive _semi_-definiteness).
- `is_symmetric` should tolerate floating-point noise (`np.allclose`, not exact equality).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`quadratic_form` is a direct translation of `x^T @ A @ x`, no cleverness needed.

</details>

<details>
<summary>Hint 2</summary>

`06-eigenvalues-eigenvectors`'s own `np.linalg.eigvalsh` sibling gives you eigenvalues without the eigenvectors, exactly what the checkable condition needs.

</details>

## Theory

### The simple version

A ball dropped into a bowl always rolls to the bottom, no matter which side you drop it from, every direction curves upward there. Drop it on a saddle-shaped surface (a mountain pass) and it rolls away in some directions but not others. "Positive-definite" is the precise mathematical statement of "this surface curves upward in every direction", the bowl case, not the saddle.

### The formula

A symmetric matrix `A` is **positive-definite** if the quadratic form `x^T A x` is strictly positive for every nonzero vector `x`:

```text
x^T @ A @ x > 0   for all x != 0
```

Checking this directly for "every possible `x`" is impossible, but there's an equivalent, checkable condition: `A` is positive-definite if and only if it is symmetric and every one of its eigenvalues (`06-eigenvalues-eigenvectors`) is strictly positive.

This matters for optimization because of the Hessian (the matrix of second partial derivatives, covered in the Calculus track): at a critical point of a function (where the gradient is zero), the Hessian being positive-definite is exactly what certifies that point as a genuine local **minimum**, not a maximum or a saddle point. Intuitively, `x^T H x > 0` for every direction `x` means the function curves upward no matter which way you step from that point, so you can't be standing at a maximum (curving down in some direction) or a saddle (curving up in some directions, down in others).

This same property is why a covariance matrix (Probability track) is always at least positive-_semi_-definite (`>= 0` instead of `> 0`): variance can never be negative, and `x^T @ Cov @ x` is exactly the variance of the projection of the data onto direction `x`.

### How PyTorch actually implements this

Optimizers that use second-order information (like L-BFGS, `torch.optim.LBFGS`) rely on this exact property: they build an approximation to the Hessian (or its inverse) and use it to take smarter steps than plain gradient descent, but that approximation is only trustworthy, and the resulting step only guaranteed to decrease the loss, when the approximated Hessian stays positive-definite. Cholesky decomposition (`torch.linalg.cholesky`) is the practical workhorse built on this property: it only succeeds on a positive-definite matrix, which is precisely why it's used as a fast validity check in libraries (a covariance matrix that fails to Cholesky-decompose signals a numerical problem upstream) and as the backbone of efficient linear-system solvers whenever the matrix involved is known to be positive-definite (a Gaussian process's kernel matrix, in `05-gaussian-processes`, is exactly such a case).

## Explanation

`is_symmetric` checks `np.allclose(a, a.T)`.

`quadratic_form` computes `x @ a @ x` directly, the definition.

`is_positive_definite` first checks `is_symmetric` (positive-definiteness is only even defined for symmetric matrices here), then computes all eigenvalues via `np.linalg.eigvalsh` and checks that every one is strictly greater than `0`, the equivalent, checkable condition from Theory.
