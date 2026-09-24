---
name: numpy-aggregations
title: Aggregations
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions computing summary statistics across an entire array using NumPy's aggregation functions, contrasted with an explicit loop.

## Theory

**Aggregation functions** reduce an array to a smaller result by combining its elements: `sum`, `mean`, `std`, `var`, `min`, `max`, `argmin` (the _index_ of the minimum), `argmax` (the _index_ of the maximum).

```python
arr = np.array([4, 8, 15, 16, 23, 42])
arr.sum()       # 108
arr.mean()      # 18.0
arr.min()       # 4
arr.argmin()    # 0 — position of the minimum, not the value
```

`min`/`max` return the actual value; `argmin`/`argmax` return the position. Each is available as both a method (`arr.sum()`) and a standalone function (`np.sum(arr)`).

Like other vectorized operations, computing an aggregation with NumPy's built-in is dramatically faster than accumulating with an explicit Python loop.

## Explanation

`compute_summary` returns a dict of `arr.sum()`, `arr.mean()`, `arr.std()`, `arr.min()`, `arr.max()`, `arr.argmin()`, `arr.argmax()` — each a direct method call. `sum_with_loop` accumulates with `total = 0` then `for value in arr: total += value`, to be compared against `arr.sum()`.
