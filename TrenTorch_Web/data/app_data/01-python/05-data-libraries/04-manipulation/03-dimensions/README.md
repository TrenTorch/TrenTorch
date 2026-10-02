---
name: numpy-adding-removing-dimensions
title: 'Adding & Removing Dimensions'
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement functions that add a new dimension of size 1 to an array, a common preparation step for broadcasting and the inverse functions that remove size-1 dimensions.

## Theory

### Adding dimensions

`np.newaxis` (inside indexing brackets) and `np.expand_dims()` (a standalone function) both insert a new size-1 dimension without changing any values.

```python
arr = np.array([1, 2, 3])        # shape (3,)
arr[:, np.newaxis]                 # shape (3, 1), column vector
arr[np.newaxis, :]                 # shape (1, 3), row vector

np.expand_dims(arr, axis=0)       # shape (1, 3)
np.expand_dims(arr, axis=1)       # shape (3, 1)
```

Since inserting a size-1 dimension doesn't change `size` (multiplying by `1` changes nothing), this is a restricted form of `reshape` and always returns a view, never a copy.

### Removing dimensions

`squeeze()` removes dimensions of size 1 from an array's shape, without changing its values or its total `size`.

```python
arr = np.zeros((1, 3, 1, 4))
arr.squeeze().shape     # (3, 4), both size-1 dimensions removed
```

Called with no arguments, it removes every size-1 dimension. An explicit `axis` argument restricts this to a specific dimension, and raises an error if that dimension isn't actually size 1:

```python
arr.squeeze(axis=0).shape     # (3, 1, 4), only axis 0 removed
arr.squeeze(axis=1)             # raises, axis 1 has size 3, not 1
```

Like `newaxis`/`expand_dims`, `squeeze()` never changes the total element count, so it follows the same view-returning behavior as the rest of this module's reshaping-family operations.

## Explanation

`to_column_vector` uses `arr[:, np.newaxis]`. `to_row_vector` uses `arr[np.newaxis, :]`. `add_dimension_at` calls `np.expand_dims(arr, axis=axis)` directly. All three are pure metadata operations, so each result shares memory with the input.

`remove_all_singleton_dims` calls `arr.squeeze()`. `remove_singleton_at` calls `arr.squeeze(axis=axis)`. Both are direct, unconditional calls, the axis-safety check (raising when a non-size-1 axis is targeted) is handled entirely by NumPy itself.
