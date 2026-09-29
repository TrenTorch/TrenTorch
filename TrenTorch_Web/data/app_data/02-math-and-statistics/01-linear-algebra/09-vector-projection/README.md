---
name: math-vector-projection
title: 'Vector Projection and Orthogonal Decomposition'
tags: [linear-algebra]
difficulty: Beginner
---

## Statement

### The problem, from first principles

"How much of vector `a` points in the same direction as vector `b`?" comes up constantly: it's the geometric idea behind a shadow, behind "how correlated are these two signals," and it's the exact operation `10-gaussian-elimination` and `12-gram-schmidt` both build on to remove one vector's overlap with another. This question implements it directly, before either of those questions needs it as a building block.

### From theory to code

Implement `project(a, b)`, returning the projection of `a` onto `b` — the component of `a` that points along `b`'s direction — then `orthogonal_component(a, b)`, the leftover part of `a` that's perpendicular to `b`. The signatures and docstrings are already in the editor.

### Constraints

- `a` and `b` are 1D NumPy arrays of the same length.
- `b` is never the zero vector (projecting onto a direction that doesn't exist is undefined).
- `project(a, b) + orthogonal_component(a, b)` must reconstruct `a` exactly (up to floating-point precision).

### Hints

<details>
<summary>Hint 1</summary>

The projection's length along `b` is `(a · b) / (b · b)` — a dot product ratio, not the dot product alone. Multiply that scalar by the vector `b` itself to get the actual projection vector.

</details>

<details>
<summary>Hint 2</summary>

Once you have `project(a, b)`, the orthogonal component is just `a` minus it — whatever's left over after removing the along-`b` part must be everything perpendicular to `b`.

</details>

## Theory

### The simple version

Imagine the sun directly overhead and a stick leaning at an angle — its shadow on the ground is the stick's **projection** onto the ground's direction. The shadow captures "how much of the stick's length actually runs along the ground"; the stick's height above the ground is what's left over, and it points straight up, perpendicular to the ground. Every vector decomposes this way relative to any other direction: a part parallel to it (the projection) and a part perpendicular to it (the orthogonal component).

### The formula

$$
\text{proj}_b(a) = \frac{a \cdot b}{b \cdot b} \, b \qquad\qquad \text{orth}_b(a) = a - \text{proj}_b(a)
$$

- `a · b` — the dot product of `a` and `b` (`02-dot-product-norms`), which is large and positive when the two vectors point in similar directions, zero when they're perpendicular, and negative when they point in roughly opposite directions.
- `b · b` — `b`'s own dot product with itself, equal to `‖b‖²` (its squared length); dividing by this is what makes the scalar `(a·b)/(b·b)` the _correct multiple_ of `b` to reach as far as `a` actually extends along that direction, rather than an arbitrary scaling.
- `proj_b(a)` — the vector result: a scaled copy of `b` itself, since "along `b`'s direction" means "some multiple of `b`."
- `orth_b(a)` — whatever remains of `a` once its along-`b` part is subtracted out; guaranteed perpendicular to `b` by construction (their dot product is exactly zero — verified directly in this question's test suite).

### Why the orthogonal component is guaranteed perpendicular

This isn't a coincidence that needs separately proving by geometry — it falls straight out of the definition. `orth_b(a) · b = (a - proj_b(a)) · b = a·b - \frac{a \cdot b}{b \cdot b}(b \cdot b) = a \cdot b - a \cdot b = 0`. Subtracting off exactly the along-`b` amount is, by construction, subtracting off all of the overlap with `b` — nothing "along `b`" can remain.

### Where this shows up

`12-gram-schmidt` builds an entire orthonormal basis by repeatedly projecting a new vector onto every previously-built basis vector and subtracting off each projection — this question's `orthogonal_component`, applied one basis vector at a time. `10-gaussian-elimination`'s row-reduction step (subtracting a multiple of one row from another to create a zero) is the same "subtract off the overlapping part" idea applied to eliminating a variable instead of a direction.

### How NumPy actually implements this

There's no dedicated `np.project` function — real code writes exactly the formula above directly: `(a @ b) / (b @ b) * b`, using `@` for the dot product between two 1D arrays (NumPy track, Module 7). This is a case where the "library call" _is_ the formula, not a hidden abstraction over it.

## Explanation

`project(a, b)` computes `(a @ b) / (b @ b)`, the scalar coefficient from Theory, and multiplies it by `b`. `orthogonal_component(a, b)` calls `project` and subtracts the result from `a`. Both functions are direct, one-line translations of the formula — the only subtlety is computing `a @ b` and `b @ b` as genuine dot products (not, say, an accidental element-wise `a * b`, which would be a vector, not the scalar the formula's ratio requires).
