---
name: potd-profile-similarity-cosine
title: 'PROFILE SIMILARITY'
tags: [linear-algebra]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Linear Algebra

---

### Story

LinkedIn's "People You May Know" starts as raw cosine similarity between two profile embedding
vectors before any graph signal is layered on top.

---

### The Math

```
cos(u, v) = (u . v) / (||u|| * ||v||)
```

### Input Format

```
d
u_1 ... u_d
v_1 ... v_d
```

### Output Format

Scalar similarity, 6 decimals.

### Constraints

- `1 <= d <= 10^4`
- Time limit: 1.0 second.

---

### Example

**Input**

```
4
1 2 0 1
2 0 1 1
```

**Output**

```
0.500000
```

## Theory

### The simple version

Cosine similarity asks whether two vectors point in the same direction, ignoring how long each one is. Two profiles with very different amounts of activity can still look very similar if their pattern of activity points the same way.

### A zero vector has no direction

Cosine similarity divides by `||u|| * ||v||`. If either vector is all zeros, that norm is `0` and
the formula is undefined: there is no direction to compare. The convention here is to output
`0.000000` rather than `NaN` or an error, since this is the single most common disputed edge case
across similarity problems.

### Identical and orthogonal vectors are exact sanity checks

A vector compared to itself gives similarity exactly `1.000000` (the angle between a vector and
itself is `0`). Two exactly orthogonal integer vectors (dot product `0`) give exactly `0.000000`,
independent of either vector's magnitude.

### Dot product and norm both reduce over the same `d`

Both the numerator and the two norms in the denominator are single passes over the same `d`-length
vectors; there is no reason to touch either vector more than once.

## Explanation

`cosine_similarity` computes `dot = u @ v`, `norm_u = np.linalg.norm(u)`, and
`norm_v = np.linalg.norm(v)`. If either norm is exactly `0`, it returns `0.0` directly instead of
dividing; otherwise it returns `dot / (norm_u * norm_v)`. Checking both norms before dividing, not
just the product `norm_u * norm_v`, guards the same zero-vector case either vector could trigger on
its own.
