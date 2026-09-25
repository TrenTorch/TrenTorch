---
name: numpy-fancy-indexing
title: Fancy Indexing
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions that select and reorder elements using integer array indices, and confirm this always produces an independent copy rather than a view.

## Theory

**Fancy indexing** means indexing with an array (or list) of integer positions, rather than a single integer, a slice, or a boolean mask.

```python
arr = np.array([10, 20, 30, 40, 50])
arr[[0, 2, 4]]     # [10, 30, 50]
arr[[3, 0, 0, 1]]  # [40, 10, 10, 20] — reordered, with a repeat
```

The positions don't need to be in order, evenly spaced, or unique. Because of this flexibility, fancy indexing **always returns a copy**, never a view — an arbitrary, possibly-repeating selection cannot be described as "a start position, a step, and a count," so NumPy must build a genuinely new buffer.

Fancy indexing extends to multiple dimensions: pass one integer array per dimension, and corresponding positions across the arrays are paired together.

```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
rows = np.array([0, 1, 2])
cols = np.array([2, 0, 1])
arr[rows, cols]     # [3, 4, 8]  — pairs (0,2), (1,0), (2,1)
```

Fancy indexing can also assign, updating the original array's buffer at the specified positions in place.

## Explanation

`select_by_indices` and `select_paired_2d` are direct fancy-index expressions (`arr[indices]`, `arr[rows, cols]`) — NumPy handles the reordering/repeating/pairing automatically. `fancy_index_is_copy` selects, mutates the first element of the result, then checks the original array is untouched, confirming the copy semantics.
