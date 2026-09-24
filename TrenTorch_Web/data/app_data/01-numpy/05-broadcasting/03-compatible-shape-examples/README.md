---
name: numpy-compatible-shape-examples
title: Compatible Shape Examples
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions that apply broadcasting across a range of realistic compatible shape combinations.

## Theory

**Scalar with any shape** — a scalar has no dimensions, so it's compatible with anything:

```python
arr * 5
```

**1D array with a matching trailing dimension** — a vector aligns against the last axis of a matrix:

```python
matrix + vector     # vector shape (3,) aligns with matrix's trailing 3
```

**Column vector with a matrix** — the vector needs an explicit size-1 trailing dimension (`newaxis`) to broadcast down the _rows_ instead of across columns:

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

`add_scalar` and `add_row_vector` are direct `+` expressions — no reshaping needed since a scalar and a matching-trailing-dimension vector already align. `add_column_vector` reshapes `col_values` to `(n, 1)` with `col_values[:, np.newaxis]` before adding, so it broadcasts down the rows rather than failing (or misaligning) against the trailing column dimension. `outer_sum` reshapes `col_values` to `(m, 1)` and `row_values` to `(1, n)` (or relies on `row_values`'s natural `(n,)` shape aligning against the trailing axis) and adds them, letting broadcasting produce every pairwise sum.
