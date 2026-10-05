---
name: numpy-aggregation-axes
title: 'Aggregation & Axes'
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions computing summary statistics across an entire array, contrasted with an explicit loop and along a specific axis of a multi-dimensional array.

## Theory

### Aggregations

**Aggregation functions** reduce an array to a smaller result by combining its elements: `sum`, `mean`, `std`, `var`, `min`, `max`, `argmin` (the _index_ of the minimum), `argmax` (the _index_ of the maximum).

```python
arr = np.array([4, 8, 15, 16, 23, 42])
arr.sum()       # 108
arr.mean()      # 18.0
arr.min()       # 4
arr.argmin()    # 0, position of the minimum, not the value
```

`min`/`max` return the actual value; `argmin`/`argmax` return the position. Each is available as both a method (`arr.sum()`) and a standalone function (`np.sum(arr)`).

Like other vectorized operations, computing an aggregation with NumPy's built-in is dramatically faster than accumulating with an explicit Python loop.

### Aggregating along an axis

By default, an aggregation collapses an entire array to a single value. The `axis` parameter collapses **only** the specified axis, keeping every other axis intact, the result has one fewer dimension than the input.

**`axis=k` means "for each fixed combination of every other index, combine all the values that differ only along axis `k`."**

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])     # shape (2, 3)

arr.sum(axis=0)     # [5, 7, 9], sums down each column, axis 0 (size 2) collapsed
arr.sum(axis=1)     # [6, 15] , sums across each row, axis 1 (size 3) collapsed
```

The specified axis disappears from the result's shape. This holds identically for `mean`, `std`, `min`, `max` and every other aggregation.

**`keepdims=True`** keeps the aggregated axis as a size-1 dimension instead of removing it:

```python
arr.sum(axis=1, keepdims=True)     # shape (2, 1), not (2,)
```

## Explanation

`compute_summary` returns a dict of `arr.sum()`, `arr.mean()`, `arr.std()`, `arr.min()`, `arr.max()`, `arr.argmin()`, `arr.argmax()`, each a direct method call. `sum_with_loop` accumulates with `total = 0` then `for value in arr: total += value`, to be compared against `arr.sum()`.

`sum_along_axis` is `arr.sum(axis=axis)`. `mean_keeping_dims` is `arr.mean(axis=axis, keepdims=True)`. `column_maxes` aggregates along `axis=0` (varying the row, fixing the column) with `matrix.max(axis=0)`. `row_argmins` aggregates along `axis=1` (varying the column, fixing the row) with `matrix.argmin(axis=1)`.
