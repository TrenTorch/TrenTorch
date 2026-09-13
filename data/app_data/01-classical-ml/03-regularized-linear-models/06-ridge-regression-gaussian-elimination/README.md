---
name: regularized-linear-models-ridge-regression-gaussian-elimination
title: 'Ridge Regression From Scratch: Solving the Normal Equation by Hand'
tags: [classical-ml, regression, numerical-methods]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`Ridge Regression (L2)` already derives the closed-form solution `theta = (X^T X + alpha I)^-1 X^T y` and hands the actual inversion to `np.linalg.inv`. That's the right call for a normal library function, but it skips the part that makes the formula reliable in the first place: `np.linalg.inv` is itself just Gaussian elimination under the hood, and elimination done naively (always using whichever row is "next," never checking its size) can divide by a pivot that's zero, or merely tiny, and either crash outright or quietly produce garbage from floating-point cancellation.

This question asks for the whole pipeline by hand: assemble ridge's normal equation yourself, then solve it with your own Gaussian elimination, one that picks the LARGEST available pivot at each step (partial pivoting) instead of whatever row happens to be next. No `np.linalg.inv`, `np.linalg.solve`, or `np.linalg.pinv` anywhere in your solution, the whole point is building the thing those functions hide.

### From theory to code

Implement two functions. `gaussian_elimination_solve(a, b)` solves the square linear system `a @ x = b` via elimination with partial pivoting, no numpy solver shortcuts. `ridge_regression_predict(input, target, lam, queries)` builds ridge's normal equation and calls your own solver to fit it, then predicts for every row of `queries`.

One convention this question uses that `Ridge Regression (L2)` does NOT: the bias column here is regularized too, no zeroing out the last diagonal entry. Simpler to reason about, and it matches how several real systems (including plain L2 weight decay applied uniformly) actually do it, contrasting with the convention seen there is itself part of the point.

### Constraints

- Append the bias column as the LAST column of the augmented design matrix (a column of ones), matching `Linear Regression: closed form (Normal Equation)`'s own convention.
- `lam` regularizes every dimension of the normal equation's identity term, including the bias position, unlike `Ridge Regression (L2)`.
- `gaussian_elimination_solve` must pivot: at each elimination step, swap in the row with the largest-magnitude entry in the current column before eliminating. A matrix that's perfectly solvable but has a zero (or tiny) pivot in its natural row order must still work.
- `lam=0` degenerates to plain least squares, solved through the same elimination path (no special-casing).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`gaussian_elimination_solve`: work on the augmented matrix `[a | b]`. At column `k`, find the row (at or below `k`) with the largest absolute value in that column, swap it into row `k`, then eliminate that column from every row below as usual. Back-substitute once the matrix is upper-triangular.

</details>

<details>
<summary>Hint 2</summary>

`ridge_regression_predict`: augment `input` with a ones column (`np.hstack`), form `a = X^T X + lam * I` and `b = X^T y` (full-size identity, no zeroing), call `gaussian_elimination_solve(a, b)` to get the combined weight+bias vector, then augment `queries` the same way and take the dot product with the solved vector.

</details>

## Theory

### The simple version

`Ridge Regression (L2)` treats "solve `A x = b`" as a black box (`np.linalg.inv`). That's usually correct, but the black box is doing something specific: turning the system into a staircase (upper-triangular) shape one column at a time, then reading the answer off the staircase from the bottom up. The one wrinkle that matters in practice: if the number you're about to divide by (the pivot) is zero or just very small, that step blows up or amplifies rounding error enormously, so a real solver always looks for the biggest available pivot first, even if that means swapping rows around.

### The formula

Ridge's normal equation, this question's convention (every dimension regularized, bias included):

$$
A = X^{\top}X + \lambda I, \qquad b = X^{\top}y, \qquad A\,\theta = b
$$

Gaussian elimination with partial pivoting solves `A theta = b` directly, without ever forming `A^{-1}`:

$$
\text{for each column } k: \quad \text{swap in } \operatorname*{arg\,max}_{i \ge k} |A_{ik}|, \quad \text{then eliminate column } k \text{ below the pivot}
$$

Once `A` is upper-triangular, back-substitution reads `theta` off from the last row upward, each row needing only the rows already solved below it. This is exactly what `np.linalg.solve` does internally (via LAPACK), just made explicit here instead of hidden behind a library call.

### How PyTorch actually implements this

`torch.linalg.solve` (and NumPy's `np.linalg.solve`) call into LAPACK's `getrf`/`getrs` routines under the hood, which are themselves partial-pivoted Gaussian elimination (LU decomposition) plus back-substitution, implemented in heavily optimized Fortran/C rather than pure Python. The algorithm is identical to what this question asks for by hand; the library version is just faster and handles edge cases (near-singular systems, larger-than-cache matrices) more carefully. Knowing what's inside `torch.linalg.solve` is exactly what makes `Positive-definite matrices, and why they matter for optimization` and `Matrix inverse, and when it does not exist` more than abstract warnings, they're describing real failure modes of this exact algorithm.

## Explanation

`gaussian_elimination_solve` builds the augmented matrix `[a | b]`, and at each column finds the largest-magnitude entry at or below the diagonal, swaps that row into place, then eliminates the column from every row below it. Once the matrix is upper-triangular, it back-substitutes from the last row upward to recover `x`. `ridge_regression_predict` augments `input` with a ones column, assembles `A = X^T X + lam * I` (full-size identity, bias included) and `b = X^T y`, solves for `theta` with `gaussian_elimination_solve`, then augments `queries` the same way and returns `queries_augmented @ theta`.
