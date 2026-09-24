---
name: numpy-newaxis-expand-dims
title: newaxis / expand_dims
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement functions that add a new dimension of size 1 to an array, a common preparation step for broadcasting.

## Theory

`np.newaxis` (inside indexing brackets) and `np.expand_dims()` (a standalone function) both insert a new size-1 dimension without changing any values.

```python
arr = np.array([1, 2, 3])        # shape (3,)
arr[:, np.newaxis]                 # shape (3, 1) — column vector
arr[np.newaxis, :]                 # shape (1, 3) — row vector

np.expand_dims(arr, axis=0)       # shape (1, 3)
np.expand_dims(arr, axis=1)       # shape (3, 1)
```

Since inserting a size-1 dimension doesn't change `size` (multiplying by `1` changes nothing), this is a restricted form of `reshape` and always returns a view, never a copy.

## Explanation

`to_column_vector` uses `arr[:, np.newaxis]`. `to_row_vector` uses `arr[np.newaxis, :]`. `add_dimension_at` calls `np.expand_dims(arr, axis=axis)` directly. All three are pure metadata operations, so each result shares memory with the input.
