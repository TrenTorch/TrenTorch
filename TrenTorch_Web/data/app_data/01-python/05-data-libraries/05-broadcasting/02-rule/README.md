---
name: numpy-broadcasting-rule
title: The Broadcasting Rule
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions that determine, given two array shapes, whether they are compatible for broadcasting and what the resulting shape would be and that apply broadcasting across a range of realistic compatible shape combinations.

## Theory

### The rule, precisely

NumPy compares two shapes **dimension by dimension, starting from the trailing (rightmost) dimension and working backward**. For each aligned pair, they're compatible if:

- They are exactly equal, **or**
- One of them is exactly `1` (stretched to match), **or**
- One array has no dimension at that position at all (shorter shape, treated as padded with `1`s on the left)

If neither dimension is `1` and they aren't equal at some aligned position, the shapes are **not** broadcastable.

```
matrix shape:  (2, 3)
addend shape:     (3,)
padded addend:  (1, 3)     ← treated as if this leading dim exists

position -1:  3 vs 3  → equal, compatible
position -2:  2 vs 1  → one side is 1, compatible

result shape: (2, 3)
```

The resulting broadcast shape takes, at each position, whichever of the two sizes is **not** `1` (or either, if equal). This applies independently at every dimension position, for any number of dimensions.

### Compatible shape examples

**Scalar with any shape**, a scalar has no dimensions, so it's compatible with anything:

```python
arr * 5
```

**1D array with a matching trailing dimension**, a vector aligns against the last axis of a matrix:

```python
matrix + vector     # vector shape (3,) aligns with matrix's trailing 3
```

**Column vector with a matrix**, the vector needs an explicit size-1 trailing dimension (`newaxis`) to broadcast down the _rows_ instead of across columns:

```python
col = np.array([10, 20, 30, 40])[:, np.newaxis]     # shape (4, 1)
matrix + col     # each row i has col[i] added to every element in that row
```

Without the `newaxis`, a plain shape-`(4,)` array would try to align against the matrix's trailing dimension, which fails unless it happens to match.

**Two arrays each stretching in a different dimension:**

```python
row = np.array([[1, 2, 3]])           # shape (1, 3)
col = np.array([[10], [20], [30]])    # shape (3, 1)
row + col                              # shape (3, 3)
```

## Explanation

Both functions pad the shorter shape with leading `1`s (using `(1,) * (len(longer) - len(shorter))` or by reversing, zipping with `itertools.zip_longest(fillvalue=1)` and reversing back) so both shapes have equal length, then walk pairs right-to-left. `are_broadcastable` returns `False` as soon as a pair is neither equal nor has a `1`; `broadcast_result_shape` takes `max(a, b)` at each aligned position (valid since compatibility guarantees one side is `1` or they're equal).

`add_scalar` and `add_row_vector` are direct `+` expressions, no reshaping needed since a scalar and a matching-trailing-dimension vector already align. `add_column_vector` reshapes `col_values` to `(n, 1)` with `col_values[:, np.newaxis]` before adding, so it broadcasts down the rows rather than failing (or misaligning) against the trailing column dimension. `outer_sum` reshapes `col_values` to `(m, 1)` and `row_values` to `(1, n)` (or relies on `row_values`'s natural `(n,)` shape aligning against the trailing axis) and adds them, letting broadcasting produce every pairwise sum.
