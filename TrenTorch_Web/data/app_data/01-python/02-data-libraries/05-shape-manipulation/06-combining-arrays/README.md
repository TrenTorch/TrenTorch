---
name: numpy-combining-arrays
title: 'Combining Arrays: concatenate, stack, hstack, vstack'
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions that combine multiple arrays into one using each of the four main combination functions, and understand precisely how they differ.

## Theory

**`np.concatenate([arrays], axis=...)`** joins arrays along an _existing_ axis — inputs must already have the same number of dimensions, matching in size on every axis except the one joined along.

**`np.stack([arrays], axis=...)`** joins arrays along a **brand-new** axis, requiring every input to have exactly the same shape. Stacking increases dimensionality by one; concatenating does not.

```python
a = np.array([1, 2, 3])     # shape (3,)
b = np.array([4, 5, 6])     # shape (3,)
np.stack([a, b])              # shape (2, 3) — new axis introduced
np.concatenate([a, b])        # shape (6,)   — same dimensionality
```

**`np.hstack`** and **`np.vstack`** are convenience wrappers around `concatenate` for 2D: `hstack` joins side-by-side (columns), `vstack` joins on top of each other (rows).

All four always return a **copy** — combining separate buffers into one fundamentally requires a fresh buffer.

## Explanation

`join_along_existing_axis` is `np.concatenate(arrays, axis=axis)`. `stack_as_new_axis` is `np.stack(arrays)`. `side_by_side` is `np.hstack([a, b])`. `stacked_vertically` is `np.vstack([a, b])`. Each is a direct call — the whole point of this topic is these functions already implement the combining logic, so no manual buffer-building is needed.
