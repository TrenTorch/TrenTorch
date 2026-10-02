---
name: linear-algebra-cosine-similarity
title: Cosine similarity
tags: [mathematics, linear-algebra, similarity]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Two vectors can be far apart in distance yet point in the same direction (a document and a copy of it repeated ten times). Cosine similarity compares only direction, ignoring length, which is why it is the default way to compare embeddings.

### From theory to code

Implement `cosine_similarity(a, b)` for two one-dimensional vectors.

### Constraints

- `a` and `b` are one-dimensional float arrays of equal length.
- Return a Python `float` in `[-1, 1]`.
- If either vector has zero length, return `0.0` rather than dividing by zero.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

The dot product measures alignment; dividing by both norms removes the effect of length.

</details>

<details><summary>Hint 2</summary>

`np.linalg.norm(v)` gives a vector's length.

</details>

## Theory

### The simple version

Think of the angle between two arrows. Same direction gives 1, perpendicular gives 0, opposite directions give -1. Scaling an arrow does not change its direction, so it does not change the score.

### The formula

$$\cos\theta = \frac{a \cdot b}{\lVert a \rVert\, \lVert b \rVert}$$

### How libraries implement this

`torch.nn.functional.cosine_similarity` and `sklearn.metrics.pairwise.cosine_similarity` do this for batches; they add a small epsilon instead of returning exactly zero for zero vectors.

## Explanation

The zero-length guard returns the convention `0.0`. The result is converted to a Python `float` so callers get a plain number rather than a NumPy scalar.
