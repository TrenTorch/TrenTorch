---
name: numpy-the-axis-parameter
title: The axis Parameter
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions applying aggregations along a specific axis of a multi-dimensional array.

## Theory

By default, an aggregation collapses an entire array to a single value. The `axis` parameter collapses **only** the specified axis, keeping every other axis intact — the result has one fewer dimension than the input.

**`axis=k` means "for each fixed combination of every other index, combine all the values that differ only along axis `k`."**

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])     # shape (2, 3)

arr.sum(axis=0)     # [5, 7, 9] — sums down each column, axis 0 (size 2) collapsed
arr.sum(axis=1)     # [6, 15]  — sums across each row, axis 1 (size 3) collapsed
```

The specified axis disappears from the result's shape. This holds identically for `mean`, `std`, `min`, `max`, and every other aggregation.

**`keepdims=True`** keeps the aggregated axis as a size-1 dimension instead of removing it:

```python
arr.sum(axis=1, keepdims=True)     # shape (2, 1), not (2,)
```

## Explanation

`sum_along_axis` is `arr.sum(axis=axis)`. `mean_keeping_dims` is `arr.mean(axis=axis, keepdims=True)`. `column_maxes` aggregates along `axis=0` (varying the row, fixing the column) with `matrix.max(axis=0)`. `row_argmins` aggregates along `axis=1` (varying the column, fixing the row) with `matrix.argmin(axis=1)`.
