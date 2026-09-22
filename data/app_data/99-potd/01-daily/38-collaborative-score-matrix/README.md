---
name: potd-collaborative-score-matrix
title: 'THE COLLABORATIVE SCORE MATRIX'
tags: [linear-algebra]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Linear Algebra

---

### Story

Spotify's collaborative-filtering recommendation score, at its absolute simplest, is one matrix
multiply between user and item embedding matrices. Every fancier recommender in this track builds on
getting this multiply right.

---

### The Math

```
R_hat = U V^T
```

### Input Format

```
n_users n_items d
U (n_users x d, row-major)
V (n_items x d, row-major)
```

### Output Format

`R_hat`, `n_users x n_items` matrix, 6 decimals.

### Constraints

- `1 <= n_users, n_items <= 500`, `1 <= d <= 128`
- Time limit: 1.0 second.

---

### Example

**Input**

```
2 3 2
1 0
0 1
2 1
1 2
0 1
```

**Output**

```
2.000000 1.000000 0.000000
1.000000 2.000000 1.000000
```

## Theory

### The simple version

A recommendation score, at its simplest, is just how well a user's taste vector lines up with an item's vector: multiply matching entries together and add up the result.

### The transpose is the whole trap

`U` and `V` are both given with shape `(rows, d)`, embedding dimension last. The score is
`U V^T`, not `U V`: `V` needs its last two axes swapped before the multiply so the shared dimension
`d` lines up between `U`'s columns and `V^T`'s rows. Using differently-shaped, non-square `U` and
`V` (as the example already does: `2 x 2` against `3 x 2`) turns a transpose bug into a dimension
mismatch instead of a silent wrong-shape pass.

### `d = 1` is still a real matrix multiply

With `d = 1`, `U` and `V` are column vectors and `U V^T` is exactly their outer product, a special
case of the same formula, not a different code path.

### Use the library's matmul, not a triple loop

At the maximum size (`500 x 500` output, `d = 128`), a hand-written triple-nested loop is far slower
than a BLAS-backed matrix multiply; `U @ V.T` in NumPy dispatches to the same optimized routine
either way.

## Explanation

`collaborative_scores` returns `U @ V.T`: NumPy transposes `V` from `(n_items, d)` to
`(d, n_items)`, then the `@` operator performs the matrix multiply, giving an
`(n_users, n_items)` result where entry `(u, i)` is the dot product of user `u`'s and item `i`'s
embeddings, exactly the `R_hat = U V^T` formula. A zero row in either `U` or `V` produces an
all-zero row or column in the output automatically, since a dot product against an all-zero vector
is `0` for every entry.
