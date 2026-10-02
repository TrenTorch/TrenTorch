---
name: numpy-splitting-arrays
title: 'Splitting Arrays: split, hsplit, vsplit'
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions that divide an array into multiple sub-arrays, the inverse operation of combining.

## Theory

**`np.split(arr, n, axis=...)`** divides `arr` into `n` equal-sized parts along the given axis, returning a list of sub-arrays. `arr`'s size along that axis must be evenly divisible by `n`, or it raises an error.

```python
arr = np.arange(12).reshape(3, 4)
np.split(arr, 3, axis=0)     # 3 arrays, each shape (1, 4)
np.split(arr, 2, axis=1)     # 2 arrays, each shape (3, 2)
```

**`np.hsplit`** and **`np.vsplit`** mirror `hstack`/`vstack`: `hsplit` splits along columns, `vsplit` splits along rows.

Each resulting sub-array is a **view** into the original — a regular, evenly-sized split can always be described as a set of regular slices.

```python
parts = np.split(arr, 3, axis=0)
parts[0][0, 0] = 99
print(arr)     # arr[0, 0] is now 99 too
```

Splitting shares memory; combining (previous topic) always copies.

## Explanation

`split_into_n_parts` is `np.split(arr, n, axis=axis)`. `split_columns` is `np.hsplit(arr, n)`. `split_result_shares_memory` performs the split and checks `np.shares_memory(parts[0], arr)` on the first resulting sub-array — `True`, since split results are views, unlike the combining functions from the previous topic.
