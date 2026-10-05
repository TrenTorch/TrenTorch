---
name: numpy-joining-splitting
title: 'Joining & Splitting Arrays'
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions that combine multiple arrays into one, understanding precisely how the main combination approaches differ and that divide an array into multiple sub-arrays as the inverse operation.

## Theory

### Joining arrays

**`np.concatenate([arrays], axis=...)`** joins arrays along an _existing_ axis, inputs must already have the same number of dimensions, matching in size on every axis except the one joined along.

**`np.stack([arrays], axis=...)`** joins arrays along a **brand-new** axis, requiring every input to have exactly the same shape. Stacking increases dimensionality by one; concatenating does not.

```python
a = np.array([1, 2, 3])     # shape (3,)
b = np.array([4, 5, 6])     # shape (3,)
np.stack([a, b])              # shape (2, 3), new axis introduced
np.concatenate([a, b])        # shape (6,)  , same dimensionality
```

**`np.hstack`** and **`np.vstack`** are convenience wrappers around `concatenate` for 2D: `hstack` joins side-by-side (columns), `vstack` joins on top of each other (rows).

All four always return a **copy**, combining separate buffers into one fundamentally requires a fresh buffer.

### Splitting arrays

**`np.split(arr, n, axis=...)`** divides `arr` into `n` equal-sized parts along the given axis, returning a list of sub-arrays. `arr`'s size along that axis must be evenly divisible by `n`, or it raises an error.

```python
arr = np.arange(12).reshape(3, 4)
np.split(arr, 3, axis=0)     # 3 arrays, each shape (1, 4)
np.split(arr, 2, axis=1)     # 2 arrays, each shape (3, 2)
```

**`np.hsplit`** and **`np.vsplit`** mirror `hstack`/`vstack`: `hsplit` splits along columns, `vsplit` splits along rows.

Each resulting sub-array is a **view** into the original, a regular, evenly-sized split can always be described as a set of regular slices.

```python
parts = np.split(arr, 3, axis=0)
parts[0][0, 0] = 99
print(arr)     # arr[0, 0] is now 99 too
```

Splitting shares memory; combining (previous topic) always copies.

## Explanation

`join_along_existing_axis` is `np.concatenate(arrays, axis=axis)`. `stack_as_new_axis` is `np.stack(arrays)`. `side_by_side` is `np.hstack([a, b])`. `stacked_vertically` is `np.vstack([a, b])`. Each is a direct call, the whole point of this topic is these functions already implement the combining logic, so no manual buffer-building is needed.

`split_into_n_parts` is `np.split(arr, n, axis=axis)`. `split_columns` is `np.hsplit(arr, n)`. `split_result_shares_memory` performs the split and checks `np.shares_memory(parts[0], arr)` on the first resulting sub-array, `True`, since split results are views, unlike the combining functions from the previous topic.
