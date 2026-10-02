---
name: math-householder-reflections
title: Householder Reflections
tags: [linear-algebra, orthogonalization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-gram-schmidt` builds an orthonormal basis by subtracting projections one vector at a time, which is easy to follow but loses accuracy when the input vectors are nearly parallel. A Householder reflection takes a different route to the same goal. It is a single mirror: pick a direction, and flip every vector across the plane perpendicular to it. With the right choice of direction, one mirror swings any chosen vector onto an axis, wiping out all of its entries except the first. Chaining a few such mirrors is how numerical libraries orthogonalize in practice. This question builds the mirror itself.

### From theory to code

Implement `householder_vector(x)`, which finds the mirror direction that sends `x` onto the first axis, `householder_matrix(v)`, which builds the full reflection matrix for a direction, and `apply_householder(v, a)`, which applies the reflection to a vector or a matrix without ever forming the matrix. The signatures and docstrings are already in the editor.

### Constraints

- `x` is a 1D array of floats. `householder_vector` returns a 1D array `v` of the same length such that reflecting `x` across the plane perpendicular to `v` gives `-sign(x[0]) * norm(x)` in the first entry and zeros elsewhere. Use `sign(0) = 1`.
- If `x` is the zero vector, return the zero vector. The reflection built from a zero direction is the identity.
- `householder_matrix(v)` returns the `n x n` matrix `I - 2 v v^T / (v^T v)`. For a zero `v` it returns the identity.
- `apply_householder(v, a)` returns the reflection of `a` for `a` a 1D vector or a 2D matrix (reflecting each column). It must not build the `n x n` reflection matrix and must not change `v` or `a`.

### Hints

<details>
<summary>Hint 1</summary>

The mirror that sends `x` to a multiple of `e1` has a direction along `x - alpha * e1`, where `alpha` is the target value. Both signs of `alpha` work in exact arithmetic, but one of them subtracts two nearly equal numbers when `x` is already close to the first axis. Choose the sign so the first entry of `v` gets larger in size, not smaller.

</details>

<details>
<summary>Hint 2</summary>

Reflecting `a` across the plane perpendicular to `v` is `a - 2 * v * (v @ a) / (v @ v)`. The product `v @ a` is one number for a vector and one number per column for a matrix, so the same line covers both cases.

</details>

## Theory

### The simple version

Stand a mirror upright and look at yourself. The mirror leaves every point on its surface exactly where it is and swaps every other point with its twin on the opposite side, so your left hand appears as a right hand and distances never change. A Householder reflection is that mirror in any number of dimensions: it keeps one flat plane fixed and flips everything else across it.

### The formula

For a nonzero direction $v$, the reflection across the plane perpendicular to $v$ is

$$
H = I - 2\,\frac{v v^{\top}}{v^{\top} v}
$$

Applied to a vector $a$, it subtracts twice the part of $a$ that lies along $v$:

$$
H a = a - 2\,\frac{v^{\top} a}{v^{\top} v}\,v
$$

- $H$ is symmetric ($H^\top = H$) and orthogonal ($H^\top H = I$), and applying it twice returns the original vector ($H^2 = I$). Its determinant is $-1$, which is what marks a reflection rather than a rotation.
- Lengths and angles are preserved, so $\lVert Ha \rVert = \lVert a \rVert$.
- Forming $H$ costs $n^2$ memory, while $Ha$ computed from the second form needs only two passes over $a$.

### Choosing the mirror direction

To send a vector $x$ onto the first axis, the result must have the same length as $x$, so the target is $\alpha e_1$ with $|\alpha| = \lVert x \rVert$. The direction that does it is

$$
v = x - \alpha\, e_1, \qquad \alpha = -\operatorname{sign}(x_1)\,\lVert x \rVert
$$

which gives $v = x + \operatorname{sign}(x_1)\lVert x \rVert\, e_1$. Picking the sign of $\alpha$ opposite to $x_1$ adds two numbers of the same sign in the first entry of $v$. The other choice would subtract two nearly equal numbers whenever $x$ already points close to the first axis, and the cancellation destroys most of the digits of $v$.

### Where this shows up in machine learning

Householder reflections are the building block of the QR factorization that `np.linalg.qr` and `torch.linalg.qr` run, and of the reductions used before an SVD or an eigenvalue solve. QR is how least-squares problems are solved stably instead of through the normal equations. Orthogonal weight parametrizations in recurrent networks use a product of a few reflections to keep a matrix exactly orthogonal throughout training.

### How NumPy/PyTorch actually implements this

LAPACK's `geqrf` (called by `np.linalg.qr`) stores the reflection directions and applies them with the second form above, never building any `H`. `torch.linalg.householder_product` rebuilds `Q` from the stored directions. `np.outer(v, v)` followed by `np.eye(n) - 2 * ... / (v @ v)` is the direct construction used here for checking.

## Explanation

`householder_vector` returns zeros for a zero input, otherwise computes the norm, takes the sign of the first entry with zero counted as positive, and adds `sign * norm` to the first entry of a copy of `x`. That is the direction `x + sign(x[0]) * norm(x) * e1` from Theory, with the sign chosen so the first entry never cancels. `householder_matrix` builds the identity minus twice the outer product of `v` with itself over `v @ v`, and returns the identity when `v` is zero because the division would otherwise be zero over zero. `apply_householder` computes `v @ a` once, which is a scalar for a vector and a row of per-column dot products for a matrix, and subtracts `2 * outer(v, ...) / (v @ v)`, so the work is linear in the size of `a` and the reflection matrix never exists.
