---
name: math-matrix-inverse
title: 'Matrix inverse, and when it does not exist'
tags: [linear-algebra, matrices]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Solving `3x = 6` for `x` is dividing both sides by 3, multiplying by the reciprocal `1/3`. The matrix version of "solve `Ax = b` for `x`" wants the same move: multiply both sides by something that undoes `A`. That something is `A`'s inverse, `A^-1`, and exactly like `1/0` doesn't exist, some matrices have no inverse at all, they've thrown away information a reciprocal-style operation would need to recover.

The question worth answering before ever computing an inverse: how do you know, cheaply, whether one exists? That's what the determinant is for, a single number that tells you, without doing the full inversion, whether `A` can be undone at all.

### From theory to code

Theory ties invertibility to a single condition: `det(A) != 0`. Implement the determinant check first, use it to guard against ever calling `np.linalg.inv` on a matrix that can't be inverted, and only then compute the actual inverse.

Implement `determinant`, `is_invertible` and `matrix_inverse` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `a` is always square.
- `is_invertible` must use a numerical tolerance, not exact equality against `0.0`.
- `matrix_inverse` must raise `np.linalg.LinAlgError` on a singular matrix rather than returning whatever `np.linalg.inv` happens to produce.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.linalg` already has a function that computes the determinant directly, you're wrapping it, not deriving cofactor expansion by hand.

</details>

<details>
<summary>Hint 2</summary>

Floating-point arithmetic almost never produces a bit-exact `0.0` for a genuinely singular matrix's determinant. `np.isclose` is the right tool, `== 0.0` is not.

</details>

## Theory

### The simple version

`3x = 6` is solved by multiplying both sides by `1/3`, the reciprocal of `3`. `Ax = b` wants the same move: something that "undoes" `A`, multiplied on both sides, to isolate `x`. That something is `A`'s inverse. And just like `1/0` doesn't exist, some matrices can't be undone at all.

### The formula

For a square matrix `A`, its inverse `A^-1` (when it exists) is the unique matrix satisfying:

```text
A @ A^-1 = A^-1 @ A = I
```

the matrix analogue of a nonzero number's reciprocal (`x * (1/x) = 1`).

The **determinant** is a single scalar computed from a square matrix that tells you exactly when the inverse exists:

```text
A is invertible  <=>  det(A) != 0
```

Geometrically, the determinant measures how much a matrix scales area (2D) or volume (3D, or higher-dimensional "volume") when it's applied as a linear transformation. A matrix with `det(A) = 0` collapses space into a lower dimension (a 2D transformation that squashes the plane onto a line, say), and a transformation that has thrown away a dimension cannot be undone, there is no way to recover the collapsed information, so no inverse can exist.

In practice, checking `det(A) == 0` exactly is unreliable, floating-point determinant computations essentially never land on a bit-exact zero even for a genuinely singular matrix, so `is_invertible` compares against zero with a tolerance instead.

### How PyTorch actually implements this

`torch.linalg.inv` (and `np.linalg.inv`, which shares the same underlying LAPACK routines) never computes a determinant-and-cofactors inverse the way a linear-algebra course teaches by hand, that approach is `O(n!)` and numerically disastrous for anything beyond tiny matrices. Real implementations use LU decomposition (`getrf`/`getri` in LAPACK): factor `A` into a lower- and upper-triangular pair, solve two triangular systems instead of one dense inversion. `torch.linalg.solve(A, b)` (solving `Ax = b` directly) is preferred over explicitly forming `A^-1` and multiplying whenever possible, forming the full inverse is both slower and less numerically stable than solving the system directly, exactly why you rarely see `.inverse()` in real training code.

## Explanation

`determinant` wraps `np.linalg.det(a)`.

`is_invertible` checks `not np.isclose(determinant(a), 0.0)`, the tolerance-based zero check from Theory.

`matrix_inverse` checks `is_invertible` first and raises `np.linalg.LinAlgError` if it's `False` (a clear, immediate failure rather than `np.linalg.inv` producing huge, garbage numbers on a near-singular matrix), then returns `np.linalg.inv(a)`.
