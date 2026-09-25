---
name: numpy-slicing-and-views
title: Slicing and What It Returns
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions using slice syntax on 1D and 2D arrays, and demonstrate the single most important fact about NumPy slicing: it returns a view, not a copy.

## Theory

Slicing an ndarray uses the same `start:stop:step` syntax as a Python list, extended across dimensions with a comma.

```python
arr = np.arange(10)
arr[2:5]        # [2, 3, 4] — stop exclusive
arr[::2]        # [0, 2, 4, 6, 8]
arr[::-1]       # reversed
```

For a 2D array, each dimension gets its own slice:

```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
arr[0:2, 1:3]     # rows 0-1, columns 1-2
arr[:, 0]          # every row, column 0 only
```

**The critical difference from Python lists:** slicing a list creates a new list with copied pointers. Slicing an ndarray does **not** copy data — it returns a **view**: a new ndarray object describing the same underlying buffer, just a different starting position/shape. Because of this, **mutating a slice mutates the original array**:

```python
arr = np.arange(6)
sl = arr[2:5]
sl[0] = 99
print(arr)      # [0, 1, 99, 3, 4, 5] — arr changed too
```

This holds transitively too: a slice of a slice is still a view into the same original buffer.

## Explanation

`slice_1d` and `extract_submatrix` are direct slice expressions. `slice_shares_memory` takes `arr[start:stop]`, sets its first element to `-1` (which writes straight into the shared buffer), and reports both the mutated slice and the mutated original — since they're views of the same data, the mutation is visible through both.
