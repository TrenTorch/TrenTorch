---
name: numpy-nan-aware-reductions
title: 'NaN-aware Reductions'
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Real arrays have holes, marked `NaN`, and one `NaN` turns a plain `sum`, `mean` or `max` into `NaN`. Implement the tools that work around holes. `summary_ignoring_nan` reports the count, mean, standard deviation, minimum and maximum of the known values, `count_missing` counts the holes along an axis, `fill_with_column_means` replaces each hole with the mean of the other values in its column, `rows_without_nan` keeps only complete rows, and `argmax_ignoring_nan` returns the position of the largest known value.

## Theory

### NaN is contagious

`NaN` ("not a number") means "unknown", and any arithmetic with an unknown is unknown:

```python
a = np.array([1.0, np.nan, 3.0])
a.sum()          # nan
a.max()          # nan
np.nansum(a)     # 4.0
np.nanmean(a)    # 2.0
```

The `nan*` family (`nansum`, `nanmean`, `nanstd`, `nanmin`, `nanmax`, `nanargmax`) skips the holes. Comparing with NaN is always false, so `a == np.nan` finds nothing: test with `np.isnan(a)`.

### Counting and masking

`np.isnan(a)` is a boolean array; `.sum()` counts the holes and `.any(axis=1)` flags rows that contain one:

```python
m = np.array([[1.0, np.nan], [3.0, 4.0]])
np.isnan(m).sum(axis=0)          # [0, 1]   holes per column
m[~np.isnan(m).any(axis=1)]      # [[3., 4.]]   complete rows only
```

### Filling

Replacing each hole with its column mean keeps the column mean unchanged and the table the same shape. With the column means `mu = np.nanmean(m, axis=0)`, the hole positions are `np.where(np.isnan(m))`, and `np.take(mu, cols)` supplies their replacements. A column that is entirely holes has no mean, so a fallback (here `0.0`) is needed.

### Empty slices

`np.nanmean` of an all-NaN slice returns `NaN` and emits a _RuntimeWarning_ ("Mean of empty slice"): the answer is correct, the warning just tells you there was nothing to average.

### How NumPy implements this

The `nan*` reductions replace NaN with the identity of the operation (0 for a sum, `inf` for a minimum) in a temporary copy, reduce, and correct the count for the mean. They are slower than the plain versions because of that copy.

## Explanation

`summary_ignoring_nan` uses the `nan*` functions on the known values (count from `np.count_nonzero(~np.isnan(a))`), and returns `NaN` statistics when nothing is known. `count_missing` sums `np.isnan` along the axis. `fill_with_column_means` computes the column means over the known values, falls back to `0.0` for all-NaN columns, and writes them into the holes of a copy. `rows_without_nan` keeps rows where no entry is NaN. `argmax_ignoring_nan` is `np.nanargmax`, or `-1` when every value is missing.
