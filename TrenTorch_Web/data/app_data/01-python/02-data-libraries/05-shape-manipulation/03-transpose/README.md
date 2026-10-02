---
name: numpy-transpose
title: transpose / .T
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions that reorder an array's axes using `.T` and `transpose()`, and a function confirming this operation returns a view.

## Theory

`.T` (and `transpose()`) reverses the order of an array's axes. For a 2D array this swaps rows and columns — `arr[i, j]` becomes `arr.T[j, i]`.

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])     # shape (2, 3)
arr.T                                        # shape (3, 2)
```

Transposing does **not** move any values in the buffer — it only changes the metadata describing how to read it. Because no data moves, `.T` always returns a view:

```python
t = arr.T
np.shares_memory(arr, t)     # True — transposing never copies
```

Mutating a transposed array mutates the original, like any view.

For arrays with more than two dimensions, `transpose()` accepts an explicit ordering of axis positions — any permutation, not just a full reversal:

```python
arr = np.zeros((2, 3, 4))
arr.transpose(1, 0, 2).shape   # (3, 2, 4) — axes 0 and 1 swapped
```

## Explanation

`transpose_2d` returns `arr.T`. `transpose_axes` returns `arr.transpose(axes)`, unpacking the tuple as positional arguments. `transpose_shares_memory` checks `np.shares_memory(arr, arr.T)` — always `True`, since transposing is purely a metadata change.
