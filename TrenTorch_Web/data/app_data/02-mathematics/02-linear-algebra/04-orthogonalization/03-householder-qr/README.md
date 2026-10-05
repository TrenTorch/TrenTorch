---
name: math-householder-qr
title: QR Factorization using Reflections
tags: [linear-algebra, orthogonalization, least-squares]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`02-householder-reflections` builds one mirror that clears a vector down to its first entry. A whole matrix is cleared the same way, one column at a time: use a mirror to zero everything below the diagonal in column 1, then ignore that row and column and do it again on what is left. After a mirror per column the matrix has become upper triangular, and the mirrors multiplied together form an orthogonal matrix. That is the QR factorization, `A = QR`, and it is the standard stable way to solve least-squares problems. This question builds the factorization and uses it to fit a line to noisy data.

### From theory to code

Implement `householder_qr(a)`, which returns the orthogonal factor `Q` and the upper-triangular factor `R`, then `back_substitution(r, y)`, which solves an upper-triangular system, then `least_squares_qr(a, b)`, which uses the first two to minimise the squared error of `a @ x - b`. The helpers from `02-householder-reflections` are already imported in the editor. The signatures and docstrings are already there too.

### Constraints

- `a` is an `m x n` float array with `m >= n`. `householder_qr` returns `(Q, R)` with `Q` of shape `m x m` and orthogonal, and `R` of shape `m x n` with exact zeros below the diagonal, such that `Q @ R` equals `a`.
- A column that is already zero below the diagonal needs no mirror. A zero column must not cause a division by zero.
- `a` must not be modified.
- `back_substitution(r, y)` takes a square upper-triangular `r` with nonzero diagonal and a 1D `y`, and returns the 1D `x` with `r @ x == y`. Solve from the last row upward with a loop, not with `np.linalg.solve`.
- `least_squares_qr(a, b)` assumes `a` has full column rank and returns the 1D `x` of length `n` that minimises the squared error. It must not form `a.T @ a`.

### Hints

<details>
<summary>Hint 1</summary>

At step `k` the mirror only touches rows `k` and below. Take the part of column `k` from row `k` down, find its mirror direction, and reflect the whole block of rows `k` and below.

</details>

<details>
<summary>Hint 2</summary>

Each mirror is its own inverse, so `A = H1 H2 ... Hn R`. Start `Q` as the identity and multiply on the right by each mirror in turn. Because every mirror is symmetric, reflecting the transpose of the relevant block of `Q` and transposing back does the multiplication.

</details>

<details>
<summary>Hint 3</summary>

Since `Q` is orthogonal, `||a x - b||` equals `||R x - Q^T b||`. Only the top `n` rows of `R` are nonzero, so the best `x` solves the top `n x n` triangle against the top `n` entries of `Q^T b`.

</details>

## Theory

### The simple version

Straightening a crumpled sheet one crease at a time is how Householder QR works. Each mirror smooths out one column completely, leaves the work already done untouched, and moves on to the next. When the last column is done the matrix is a clean staircase, and the stack of mirrors you used records exactly how it was straightened.

### The formula

Let $H_k$ be the mirror that zeros column $k$ below the diagonal, acting only on rows $k$ onward. Applying all of them gives

$$
H_n \cdots H_2 H_1\, A = R
$$

where $R$ is upper triangular. Each $H_k$ is symmetric and orthogonal, so inverting the product reverses the order:

$$
A = H_1 H_2 \cdots H_n\, R = Q R, \qquad Q = H_1 H_2 \cdots H_n
$$

and $Q$ is orthogonal because it is a product of orthogonal matrices. The work is about $2mn^2 - \tfrac{2}{3}n^3$ operations for an $m \times n$ matrix.

### Least squares without the normal equations

To minimise $\lVert Ax - b \rVert_2$, note that multiplying by the orthogonal $Q^\top$ does not change a length:

$$
\lVert Ax - b \rVert = \lVert Q^\top (Ax - b) \rVert = \lVert Rx - Q^\top b \rVert
$$

Only the top $n$ rows of $R$ contain anything. Writing $R_1$ for that $n \times n$ triangle and $c = (Q^\top b)_{1:n}$, the minimiser solves

$$
R_1 x = c
$$

which is solved by **back substitution** from the last row up: $x_n = c_n / r_{nn}$, then $x_{n-1}$ from row $n-1$, and so on. The remaining entries of $Q^\top b$ are the part of $b$ that no choice of $x$ can reach, so their size is the residual.

The usual shortcut, the normal equations $A^\top A x = A^\top b$, squares the condition number of $A$ and loses about half the digits that this route keeps.

### Where this shows up in machine learning

Linear regression solvers use QR rather than the normal equations for exactly this reason. Orthogonal initializations of weight matrices are taken from the `Q` of a random matrix. QR iterations are the basis of the standard eigenvalue algorithm, and the factorization appears inside many second-order and natural-gradient methods.

### How NumPy/PyTorch actually implements this

`np.linalg.qr(a, mode='complete')` returns the same factorization from LAPACK's Householder routines, up to the signs of the columns of `Q` and the rows of `R`. `np.linalg.lstsq` and `torch.linalg.lstsq` solve least squares through QR or the SVD rather than the normal equations. `scipy.linalg.solve_triangular` is the back-substitution step.

## Explanation

`householder_qr` copies `a` into `R` and starts `Q` as the identity, then for each column `k` takes the mirror direction of `R[k:, k]` from `householder_vector`. If that direction is the zero vector the column needs no work, so the step is skipped. Otherwise it reflects the block `R[k:, :]` with `apply_householder` and updates `Q` by reflecting the transpose of `Q[:, k:]` and transposing back, which is multiplication by the symmetric mirror on the right. Entries that are zero in exact arithmetic are set to exact zeros afterwards so `R` is genuinely triangular. `back_substitution` walks from the last row to the first, subtracting the already-known entries times their coefficients and dividing by the diagonal. `least_squares_qr` factors `a`, computes `Q.T @ b`, and back-substitutes on the top `n x n` triangle against the top `n` entries, never forming `a.T @ a`.
