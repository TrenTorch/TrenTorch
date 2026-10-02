---
name: math-rank-and-nullity
title: 'Rank of a Matrix and the Rank-Nullity Theorem'
tags: [linear-algebra]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`05-matrix-inverse` established that some matrices simply have no inverse. **Rank** is the precise number that tells you exactly why, and exactly how badly: it counts how many of a matrix's rows (or, equivalently, columns) are genuinely independent, rather than being a combination of the others. A square matrix has an inverse exactly when its rank equals its size; anything less, and the matrix is throwing away information that can never be recovered, which is exactly what a missing inverse means.

### From theory to code

Implement `rank(A)`, computing the number of independent rows of `A`, then `nullity(A)`, computing `A`'s number of columns minus its rank — the size of the space of vectors `A` maps to zero. The signature and docstring are already in the editor.

### Constraints

- `A` is an `m × n` NumPy array (not necessarily square).
- Compute rank via row-reduction (`10-gaussian-elimination`'s approach, extended to handle non-square, rank-deficient inputs by skipping a column entirely when every remaining candidate pivot in it is zero), not by calling `np.linalg.matrix_rank` directly — the point is to see rank fall directly out of row-reduction, not to treat it as a library black box.
- Use a small numerical tolerance (e.g. `abs(value) < 1e-10` counts as zero) rather than exact equality, since floating-point row-reduction rarely produces an exact `0.0`.

### Hints

<details>
<summary>Hint 1</summary>

Row-reduce `A` to echelon form exactly as in `10-gaussian-elimination`, but track a **pivot column pointer** separately from the row you're working on — when a column has no usable (non-zero, above tolerance) pivot in any remaining row, move on to the next column without advancing the row pointer, since that column contributed no new independent direction.

</details>

<details>
<summary>Hint 2</summary>

The rank is simply the number of pivots actually found by the time row-reduction finishes — count them as you go, rather than trying to infer the count from the shape of the final result afterward.

</details>

## Theory

### The simple version

Three rows that each point in a genuinely different direction span a 3-dimensional space; three rows where the third happens to just be the first plus the second span only a 2-dimensional space, no matter how the numbers happen to look written out — the third row carries no new information. **Rank** counts how many of a matrix's rows (or columns — the two counts are always equal, a fact called the rank theorem) are actually contributing independent directions, versus how many are redundant combinations of the others.

### The formula

$$
\text{rank}(A) + \text{nullity}(A) = n
$$

where `A` has `n` columns.

- `rank(A)` — the number of linearly independent rows (equivalently, columns) of `A`; the dimension of the space `A`'s columns actually span.
- `\text{null}(A)` — the **null space**: every vector `x` such that `Ax = 0`. `A` maps every vector in its null space to exactly the zero vector, meaning that entire direction's information is destroyed by `A`.
- `nullity(A)` — the null space's dimension: how many independent directions get collapsed to zero.
- This is the **Rank-Nullity Theorem**: every one of `A`'s `n` input dimensions is accounted for by exactly one of two fates — either it survives as part of `A`'s genuinely `rank(A)`-dimensional output, or it's one of `nullity(A)` directions collapsed entirely to zero. There's no third option and no double-counting, which is exactly why the two numbers always add up to `n`.

### Why row-reduction reveals rank directly

Row-reducing `A` never changes which linear combinations of the rows equal zero (each elimination step only ever replaces a row with itself minus a multiple of another, an operation that preserves every such relationship) — it just makes those relationships visible as literal zero rows. The number of genuinely non-zero rows remaining after full row-reduction is therefore exactly the number of independent rows the original matrix had, which is `rank(A)` by definition.

### Where this shows up

- **`05-matrix-inverse`**: an `n × n` matrix is invertible exactly when `rank(A) = n` (**full rank**) — equivalently, when `nullity(A) = 0`, meaning no input direction is ever destroyed, which is precisely what makes "undoing" `A` with an inverse possible at all.
- **`07-svd`**: the number of non-zero singular values a matrix has is exactly its rank — SVD is, among other things, a numerically robust way to compute rank in the presence of floating-point noise, where a "should be zero" pivot from naive row-reduction might come out as a tiny non-zero number instead.
- **Solving `Ax = b`** (`10-gaussian-elimination`): the system has a unique solution only when `A` is full rank; a positive nullity means either no solution exists, or infinitely many do (differing by any vector in the null space), depending on `b`.

### How NumPy actually implements this

`np.linalg.matrix_rank(A)` computes rank using SVD internally (counting singular values above a tolerance), which is more numerically robust than naive row-reduction for nearly-rank-deficient matrices, but computes the exact same mathematical quantity this question's row-reduction approach does for well-conditioned inputs.

## Explanation

`rank(A)` row-reduces a working copy of `A` to echelon form, maintaining a separate pivot-row and pivot-column pointer: for each column, it looks for a row (at or below the current pivot row) with a magnitude above the numerical tolerance to use as a pivot; if none exists, that column is skipped (it contributed no new independent direction) without advancing the row pointer, and if one does, it's used to eliminate every entry below it exactly as in `10-gaussian-elimination`, and the pivot count increments. The final pivot count is `A`'s rank. `nullity(A)` is simply `A.shape[1] - rank(A)`, a direct one-line application of the Rank-Nullity Theorem's formula.
