---
name: math-qr-decomposition
title: 'QR Decomposition'
tags: [linear-algebra]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`12-gram-schmidt` turns a set of vectors into an orthonormal basis, one vector at a time, discarding the "how much of each original vector was removed" bookkeeping along the way. QR decomposition is Gram-Schmidt with that bookkeeping kept: the orthonormal basis becomes matrix `Q`, and exactly how each original column was built from it becomes matrix `R` — together, `Q` and `R` capture the same information as the original matrix, just split into an orthogonal part and a triangular part.

### From theory to code

Implement `qr_decompose(A)`, returning `(Q, R)` such that `A = QR`, built directly from `12-gram-schmidt`'s orthonormalization process applied column-by-column. The signature and docstring are already in the editor.

### Constraints

- `A` is an `m × n` NumPy array whose columns are linearly independent (a requirement Gram-Schmidt itself already assumes).
- `Q`'s columns are orthonormal (`12-gram-schmidt`'s output).
- `R` is upper-triangular.
- `Q @ R` must reconstruct `A` exactly (up to floating-point precision).

### Hints

<details>
<summary>Hint 1</summary>

Apply Gram-Schmidt to `A`'s columns one at a time to get `Q`'s columns. `R`'s entries are exactly the projection coefficients Gram-Schmidt computes and subtracts along the way — record them instead of throwing them away.

</details>

<details>
<summary>Hint 2</summary>

`R[i, j]` (for `i <= j`) is the dot product of `Q`'s `i`-th column with `A`'s original `j`-th column; `R[j, j]` specifically is the norm of what's left of column `j` after subtracting off its projections onto every earlier `Q` column, before that leftover gets normalized into `Q`'s `j`-th column.

</details>

## Theory

### The simple version

Gram-Schmidt (`12-gram-schmidt`) builds an orthonormal basis by, for each new vector, subtracting off its overlap with every previously-built basis vector and normalizing what's left. QR decomposition notices that "how much overlap was subtracted" and "how much was left to normalize" are themselves useful numbers worth keeping, not throwing away — arranged into a matrix, they reconstruct the original columns exactly from the orthonormal basis.

### The formula

$$
A = QR
$$

- `Q` — an `m × n` matrix whose columns are orthonormal (Gram-Schmidt's output directly).
- `R` — an `n × n` upper-triangular matrix, where `R[i, j]` (`i < j`) is column `j`'s projection coefficient onto `Q`'s `i`-th column, and `R[j, j]` is the norm of column `j`'s leftover component after all earlier projections are removed.

Column `j` of `A` can be written as `A[:, j] = R[0,j] Q[:, 0] + R[1,j] Q[:, 1] + \cdots + R[j,j] Q[:, j]` — exactly `Q`'s first `j+1` columns, scaled by the coefficients that reconstruct `A`'s `j`-th column from them. This is precisely what makes `R` upper-triangular: column `j` of `A` only ever needs `Q`'s columns up to and including `j`, never any later one.

### Why this decomposition is useful

Because `Q`'s columns are orthonormal, `Qᵀ Q = I` — multiplying by `Qᵀ` "undoes" `Q` for free, without needing an actual matrix inverse. Solving `Ax = b` via `QRx = b` gives `Rx = Qᵀb`, a triangular system solved by back substitution (`11-lu-decomposition`'s idea, one triangular factor instead of two) — this is the standard, numerically stable way to solve **least-squares problems** (more equations than unknowns), which come up constantly in fitting a model to noisy data.

### Where this shows up

`05-numerical-computation`'s "Linear least squares, solved three ways" question implements QR as one of the three solution paths to the same fitting problem, contrasted directly against the normal-equations approach (which squares `A`, amplifying any numerical error) and SVD (`07-svd`, the most robust but most expensive of the three).

### How NumPy/SciPy actually implements this

`np.linalg.qr(A)` computes this decomposition using a different, more numerically stable algorithm internally (Householder reflections, not literal Gram-Schmidt, which can lose orthogonality due to floating-point rounding when applied naively to many columns) — but the mathematical result, and what `Q` and `R` mean, is identical to what this question builds directly.

## Explanation

`qr_decompose` builds `Q` one column at a time using `12-gram-schmidt`'s exact projection-and-subtract process, but additionally records, for each earlier `Q` column `i` and current column `j`, the projection coefficient `Q[:, i] @ A[:, j]` into `R[i, j]` — this is the same number Gram-Schmidt already computes internally to know how much to subtract. After subtracting off every earlier projection, the leftover vector's norm is recorded as `R[j, j]` before that leftover is normalized (divided by its own norm) to become `Q`'s `j`-th column. Every entry above the diagonal in `R` is filled this way; every entry below stays `0` by construction, since column `j` of `A` never contributes to any `R` entry in a row past `j`.
