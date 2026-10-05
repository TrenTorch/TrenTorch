---
name: numpy-conditional-replacement
title: 'Conditional Replacement & Clipping'
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement functions that change array values depending on a condition, without a Python loop. `replace_where` returns a copy in which the positions selected by a boolean mask take a given value, `clip_to_percentiles` limits every value to the range between two percentiles of the data (a standard way to tame outliers), `sign_class` labels each value -1, 0 or 1 by its sign, and `bucket_label` maps values to three labels using several conditions at once.

## Theory

### `np.where` chooses element by element

`np.where(condition, x, y)` returns `x` where the condition is true and `y` elsewhere, as a new array:

```python
a = np.array([5, -2, 7, -1])
np.where(a < 0, 0, a)      # [5, 0, 7, 0]   negatives replaced by 0
```

Assigning through a mask does the same in place: `a[a < 0] = 0` changes `a`, whereas `np.where` leaves it untouched. Work on a copy when the caller's array must not change.

### Clipping

`np.clip(a, lo, hi)` forces every value into `[lo, hi]`: values below `lo` become `lo`, above `hi` become `hi`. Choosing the limits from the data itself, the 5th and 95th percentile for example, is called **winsorising**:

```python
lo, hi = np.percentile(a, [5, 95])
np.clip(a, lo, hi)
```

It reduces the influence of extreme values while keeping every observation.

### Several conditions

`np.select(condlist, choicelist, default)` generalises `where` to many branches. The conditions are checked in order and the **first** true one wins, like an `if / elif / else` applied to a whole array:

```python
np.select([a < 0, a == 0], [-1, 0], default=1)   # the sign
```

For plain signs, `np.sign(a)` also works.

### How NumPy implements this

`where`, `clip` and `select` are vectorised loops in C that read each element once and write a new array, so they cost one pass over the data. A boolean mask used as an index builds a new array from the selected positions.

## Explanation

`replace_where` copies the array and writes the value through the mask (or uses `np.where`). `clip_to_percentiles` computes the two percentile values with linear interpolation and clips the array to them. `sign_class` evaluates the negative and zero cases in order and defaults to 1. `bucket_label` applies the thresholds with `np.select`, where the first matching condition decides.
