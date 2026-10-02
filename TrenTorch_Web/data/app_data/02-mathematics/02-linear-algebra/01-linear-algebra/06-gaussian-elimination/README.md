---
name: math-gaussian-elimination
title: 'Solving Linear Systems by Hand: Gaussian Elimination'
tags: [linear-algebra]
difficulty: Intermediate
widget: row-reduction-stepper
---

## Statement

### The problem, from first principles

`05-matrix-inverse` computes `A⁻¹` and uses it to solve `Ax = b`, but never explains _how_ an inverse (or a solution) is actually found by hand in the first place — it's presented as a formula to apply, not a procedure. Gaussian elimination is that procedure: a systematic way to reduce a system of equations, step by step, until the answer is directly readable off the result. It's also the exact mechanism behind `11-lu-decomposition` and behind why `05-matrix-inverse`'s inverse fails to exist for some matrices.

### From theory to code

Implement `gaussian_eliminate(A, b)`, reducing the augmented system `[A | b]` to upper-triangular form via row operations, then `back_substitute(U, c)`, solving the resulting triangular system for `x`. The signatures and docstrings are already in the editor.

### Constraints

- `A` is a square `n × n` NumPy array; `b` is a length-`n` NumPy array.
- Assume no row swaps are needed (every pivot encountered is non-zero) — the same assumption `11-lu-decomposition` makes.
- `gaussian_eliminate` returns the reduced augmented system as `(U, c)`: `U` upper-triangular, `c` the correspondingly transformed right-hand side.
- `back_substitute` returns the solution vector `x` such that `Ux = c`.

### Hints

<details>
<summary>Hint 1</summary>

Work on a combined copy of `A` and `b` together (or keep them as two separate arrays updated in lockstep) — every row operation applied to eliminate a variable in `A` must be applied identically to the corresponding entry of `b`, since they represent the same equation.

</details>

<details>
<summary>Hint 2</summary>

For back substitution, solve for the **last** variable first (its row has only one unknown left), then substitute that known value into the row above to solve for the next variable, working upward — the reverse order of how elimination worked downward.

</details>

## Theory

### The simple version

Solving `2x + y = 5` and `x - y = 1` by hand, the "obvious" approach is to manipulate the equations until one variable disappears — add the two equations together and `y` cancels, leaving `3x = 6`, so `x = 2`, then substitute back to get `y = 1`. Gaussian elimination is exactly this "combine equations to cancel a variable" instinct, made completely systematic: eliminate one variable at a time, from as many equations as possible, until every equation has only one unknown left.

### The formula

**Elimination step**, for pivot row `j` and every row `i` below it:

$$
\text{multiplier} = \frac{A_{ij}}{A_{jj}}, \qquad \text{row}_i \leftarrow \text{row}_i - \text{multiplier} \times \text{row}_j
$$

applied identically to `b_i`. After running this for every pivot column, `A` becomes upper-triangular (`U`) and `b` becomes the correspondingly transformed `c`.

**Back substitution**, once `Ux = c` is upper-triangular, solving from the bottom row up:

$$
x_i = \frac{c_i - \sum_{k > i} U_{ik} x_k}{U_{ii}}
$$

- `multiplier` — exactly the number that makes row `i`'s entry in the pivot column become zero when subtracted; this is the same number `11-lu-decomposition` records into `L` instead of discarding.
- The back-substitution sum `Σ_{k>i}` (`01-summation-notation`) subtracts off the contribution of every already-solved-for variable to the right of `x_i`, leaving only `x_i`'s own coefficient to divide out.

### Watch the row-reduction stepper below

<div class="tt-widget" data-widget="row-reduction-stepper">
	<div class="matrix-grid"></div>
	<div class="controls">
		<div class="btnrow">
			<button class="wbtn" id="stepBackBtn" type="button">← Step</button>
			<button class="wbtn primary" id="stepForwardBtn" type="button">Step →</button>
		</div>
		<button class="wbtn" id="resetBtn" type="button">Reset</button>
		<div class="readout">
			<div>Step <b id="stepLabel">0 / 0</b></div>
		</div>
		<div id="stepDescription" style="font-size: 12.5px; color: var(--muted-foreground, #a1a1aa)">
		</div>
	</div>
</div>

Step through eliminating the example system `2x + y - z = 8`, `-3x - y + 2z = -11`, `-2x + y + 2z = -3` (solution `x=2, y=3, z=-1`) — the highlighted cell is the current pivot; amber cells are the ones that step just changed.

### Why this always works (given the no-row-swap assumption)

Every row operation used here (subtracting a multiple of one row from another) is **reversible** and never changes the system's solution set — it's exactly the same operation as this track's `09-vector-projection`'s "subtract off the overlapping part" idea, applied to entire equations instead of vectors. Since the operation is reversible, the reduced system `Ux = c` has exactly the same solutions as the original `Ax = b`, and a triangular system is trivial to solve directly by back substitution.

### Where this shows up

This entire procedure, split into its two named ingredients, reappears as `11-lu-decomposition` (elimination, with multipliers kept instead of discarded) and is exactly what `np.linalg.solve` runs internally (with additional row-swapping for numerical stability, a refinement this question's constraints deliberately set aside).

### How NumPy actually implements this

`np.linalg.solve(A, b)` performs this same elimination-then-back-substitution procedure (via LAPACK's LU-with-partial-pivoting routines) rather than ever explicitly forming `A⁻¹` — precisely the reasoning the NumPy track's own `np.linalg.solve` question covers directly.

## Explanation

`gaussian_eliminate` works on float copies of `A` and `b` so the caller's arrays are never mutated, looping over pivot columns `j` and, for each row `i` below it, computing `multiplier = U[i, j] / U[j, j]`, then subtracting `multiplier * U[j]` from `U[i]` and `multiplier * c[j]` from `c[i]` in lockstep — the same elimination step as `11-lu-decomposition`, minus the bookkeeping of recording multipliers into `L`. `back_substitute` walks rows from the last to the first, computing each `x[i]` as `(c[i] - U[i, i+1:] @ x[i+1:]) / U[i, i]` — a direct translation of the back-substitution formula, using already-solved entries of `x` for every coefficient to the right of the diagonal.
