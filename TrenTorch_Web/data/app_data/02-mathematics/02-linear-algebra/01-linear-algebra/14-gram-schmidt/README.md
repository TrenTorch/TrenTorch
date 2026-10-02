---
name: math-gram-schmidt
title: 'Gram-Schmidt Orthogonalization'
tags: [linear-algebra]
difficulty: Advanced
widget: vector-orthogonalization-animator
---

## Statement

### The problem, from first principles

Many useful properties (`13-qr-decomposition`'s stable solving, an orthonormal basis's trivially-invertible-by-transpose structure) only apply when a set of vectors is not just independent, but **orthonormal**: mutually perpendicular, each of unit length. Most real vector sets you're handed aren't — Gram-Schmidt is the direct procedure for turning any independent set into an orthonormal one, one vector at a time, using nothing but `09-vector-projection`'s "subtract off the overlapping part" idea repeated against every earlier result.

### From theory to code

Implement `gram_schmidt(vectors)`, taking a list of linearly independent vectors and returning an orthonormal basis spanning the same space. The signature and docstring are already in the editor.

### Constraints

- `vectors` is a list of 1D NumPy arrays, all the same length, guaranteed linearly independent.
- Return a list of the same length, each entry a unit vector (`‖v‖ = 1`), with every pair mutually orthogonal (`v_i · v_j = 0` for `i ≠ j`).
- Process vectors in the given order — the resulting basis depends on that order (a different input order generally produces a different, still valid, orthonormal basis).

### Hints

<details>
<summary>Hint 1</summary>

For each new vector, subtract its projection (`09-vector-projection`) onto **every** already-built basis vector, not just the most recent one — each earlier basis vector may capture a different direction of overlap.

</details>

<details>
<summary>Hint 2</summary>

Only normalize (divide by the norm) **after** all of that vector's projections onto earlier basis vectors have been subtracted — normalizing too early would rescale the vector before its remaining overlap has been fully removed.

</details>

## Theory

### The simple version

Given two directions that aren't perpendicular, keep the first exactly as it is, then take the second and subtract off "however much of it points the same way as the first" (`09-vector-projection`) — what's left is guaranteed perpendicular to the first. Scale both to length `1` and you have an orthonormal pair. With three or more vectors, repeat the same subtraction against every previously-built vector before moving to the next.

### The formula

For input vectors `v_1, \ldots, v_k`, build orthonormal `u_1, \ldots, u_k` one at a time:

$$
w_i = v_i - \sum_{j < i} \text{proj}_{u_j}(v_i), \qquad u_i = \frac{w_i}{\|w_i\|}
$$

- `proj_{u_j}(v_i)` — `09-vector-projection`'s projection of `v_i` onto the `j`-th already-built basis vector.
- `Σ_{j<i}` — subtract off the overlap with **every** earlier basis vector, not just the most recent one (`01-summation-notation`'s `Σ` applied to a sum of vectors, not scalars).
- `w_i` — what's left of `v_i` after removing every earlier direction's overlap; guaranteed orthogonal to all of `u_1, \ldots, u_{i-1}` by the same reasoning `09-vector-projection`'s Theory used to show a single orthogonal component is perpendicular.
- `u_i` — `w_i` normalized to length `1`.

### Watch the animation below

<div class="tt-widget" data-widget="vector-orthogonalization-animator">
	<canvas id="voacanvas"></canvas>
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

Green arrows are the orthonormal basis built so far; red is the vector currently being processed; the dashed amber arrow is the projection being subtracted off it.

### Why the order matters

Since each new vector's projections are only taken against the basis vectors already built, processing `[v_1, v_2]` versus `[v_2, v_1]` produces two different (but equally valid) orthonormal bases — the first vector processed always survives with only its own length normalized, never having anything subtracted from it, while a vector processed later has progressively more removed from it. Neither basis is "more correct" than the other; both span the same space orthonormally, they're just built along a different starting direction.

### Where this shows up

`13-qr-decomposition` is this exact process with the subtracted coefficients kept instead of discarded — `Q` is literally this question's output, and `R` is the bookkeeping this question's Theory mentions but doesn't need to keep.

### How NumPy/SciPy actually implements this

`np.linalg.qr(A)` produces an orthonormal basis via a different, more numerically stable algorithm (Householder reflections) — naive Gram-Schmidt, run on many vectors in floating point, can gradually lose orthogonality due to accumulated rounding error (a phenomenon called "loss of orthogonality"), which is precisely why production code doesn't implement literal Gram-Schmidt for anything beyond a small, illustrative case like this one.

## Explanation

`gram_schmidt` builds up a `basis` list one input vector at a time. For each `v`, it starts `w = v.copy()` and repeatedly subtracts `09-vector-projection`'s projection of the **current, running** `w` onto each already-built basis vector `u`, one `u` at a time. This gives the same final result as projecting the original `v` against every `u` and subtracting all of them at once, because each `u` already in `basis` is orthogonal to every earlier one — subtracting `w`'s overlap with an earlier `u` never disturbs the component along a later `u` that hasn't been subtracted yet. Once every earlier overlap has been removed, `w` is divided by its own norm and appended to `basis`. Processing vectors strictly in the given order, and only normalizing after all subtractions for that vector are complete, is what guarantees the result is genuinely orthonormal rather than merely close to it.
