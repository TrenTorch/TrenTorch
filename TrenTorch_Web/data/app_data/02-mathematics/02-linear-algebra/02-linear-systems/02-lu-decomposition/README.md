---
name: math-lu-decomposition
title: 'LU Decomposition'
tags: [linear-algebra]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`10-gaussian-elimination` solves `Ax = b` by row-reducing `A` down to an upper-triangular form. But that same row-reduction work is thrown away the moment you need to solve a **different** `b` with the **same** `A`, a common situation (simulating many right-hand sides against one fixed system matrix). LU decomposition captures the row-reduction work itself as two reusable matrices, so solving for a new `b` afterward is nearly free.

### From theory to code

Implement `lu_decompose(A)`, returning `(L, U)` such that `A = LU`, using the exact row-elimination steps from `10-gaussian-elimination` but recording each elimination multiplier into `L` instead of discarding it. The signature and docstring are already in the editor.

### Constraints

- `A` is a square `n × n` NumPy array that does not require row swaps (a **partial pivoting**-free case, real solvers handle the swap case too, but that's a refinement on top of this question's core idea, not covered here).
- `L` is lower-triangular with `1`s on its diagonal; `U` is upper-triangular.
- `L @ U` must reconstruct `A` exactly (up to floating-point precision).

### Examples

**Example 1** (2 × 2)

```
A = [[4, 3],
     [6, 3]]
```

Zero out `A[1, 0]` using pivot row 0: the multiplier is `6 / 4 = 1.5`. Subtract `1.5 * row 0` from row 1, giving `[6 - 6, 3 - 4.5] = [0, -1.5]`.

```
L = [[1.0, 0.0],      U = [[4.0,  3.0],
     [1.5, 1.0]]           [0.0, -1.5]]
```

Check: `L @ U = [[4, 3], [1.5 * 4, 1.5 * 3 - 1.5]] = [[4, 3], [6, 3]]`.

**Example 2** (3 × 3)

```
A = [[2, 1, 1],
     [4, 3, 3],
     [8, 7, 9]]
```

- Column 0, pivot `2`: multipliers `4 / 2 = 2` for row 1 and `8 / 2 = 4` for row 2. Row 1 becomes `[0, 1, 1]`, row 2 becomes `[0, 3, 5]`.
- Column 1, pivot `1`: multiplier `3 / 1 = 3` for row 2. Row 2 becomes `[0, 0, 2]`.

```
L = [[1, 0, 0],       U = [[2, 1, 1],
     [2, 1, 0],            [0, 1, 1],
     [4, 3, 1]]            [0, 0, 2]]
```

Each multiplier sits in `L` at the position of the entry it zeroed out: `L[1, 0] = 2`, `L[2, 0] = 4`, `L[2, 1] = 3`.

### Hints

<details>
<summary>Hint 1</summary>

Start `U` as a copy of `A` and `L` as the identity matrix. Run the same elimination loop as `10-gaussian-elimination` on `U`, but every time you compute a multiplier to zero out an entry, also write that exact multiplier into the corresponding position of `L`.

</details>

<details>
<summary>Hint 2</summary>

The multiplier that zeros out `U[i, j]` using pivot row `j` is `U[i, j] / U[j, j]`; this is precisely the number that belongs at `L[i, j]`.

</details>

## Theory

### The simple version

Row-reducing a matrix to upper-triangular form is really a sequence of "subtract a multiple of an earlier row from a later row" steps. LU decomposition's insight: instead of throwing those multipliers away once you've used them, write each one down in exactly the position it came from. The multipliers collected this way, arranged below the diagonal with `1`s on the diagonal, turn out to _exactly_ undo the elimination, multiplying them back in (`L`) against the eliminated result (`U`) reconstructs the original matrix precisely.

### The formula

$$
A = LU
$$

- `L`: lower-triangular, `1`s on the diagonal, off-diagonal entries below the diagonal are the elimination multipliers.
- `U`: upper-triangular, the row-echelon result of eliminating `A` exactly as in `10-gaussian-elimination`.

### Why this makes solving with a new `b` fast

Once `A = LU` is known, solving `Ax = b` becomes `LUx = b`. Set `y = Ux`, and solve `Ly = b` first: because `L` is lower-triangular, this is solved top-to-bottom in one pass (**forward substitution**) with no elimination needed at all. Then solve `Ux = y` bottom-to-top (**back substitution**), again no elimination. Both substitution passes are `O(n²)`, dramatically cheaper than the `O(n³)` elimination that computing `L` and `U` cost in the first place, a cost paid once, then reused for every subsequent `b`.

### Where this shows up

Any workflow solving `Ax = b_1, Ax = b_2, \ldots` against the same `A` repeatedly (a common pattern in simulation and control systems) computes the LU decomposition once and reuses it, rather than re-running full Gaussian elimination from scratch for every new right-hand side.

### How NumPy/SciPy actually implements this

`scipy.linalg.lu(A)` computes this decomposition directly (including the row-swap handling this question's constraints deliberately avoid, via an additional permutation matrix `P` such that `PA = LU`), and `scipy.linalg.lu_solve` uses a precomputed decomposition to solve new right-hand sides via forward/back substitution, exactly as described above. `np.linalg.solve` itself uses LU decomposition with pivoting internally; it is not a fundamentally different algorithm from what this question implements, just a more numerically robust version of it.

## Explanation

`lu_decompose` initializes `U` as a float copy of `A` (so in-place modifications never mutate the caller's array) and `L` as the `n × n` identity matrix. It then loops over pivot columns `j`, and for each row `i` below the pivot, computes the multiplier `U[i, j] / U[j, j]`, stores it directly at `L[i, j]`, and subtracts `multiplier * U[j]` from row `U[i]`; the same elimination step as `10-gaussian-elimination`, except the multiplier is written into `L` instead of being a throwaway local variable. By the time every column has been eliminated, `U` is upper-triangular and `L`'s recorded multipliers are exactly what's needed to reconstruct `A` when multiplied back through `L @ U`.
