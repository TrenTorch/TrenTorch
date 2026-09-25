---
name: numpy-shape-ndim-size
title: shape, ndim, size
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement a function that reads and reports an array's structural metadata, and a function that validates whether a given shape is consistent with a given element count.

## Theory

Every ndarray carries three pieces of structural metadata:

- **`shape`** — a tuple giving the size of each dimension. A 1D array of length 5 has shape `(5,)`; a 2D array with 3 rows and 4 columns has shape `(3, 4)`.
- **`ndim`** — the number of dimensions, equal to `len(shape)`.
- **`size`** — the total number of elements, equal to the product of every value in `shape`.

```python
arr = np.zeros((3, 4))
arr.shape     # (3, 4)
arr.ndim      # 2
arr.size      # 12
```

These are always consistent: `ndim == len(shape)`, and `size` equals the product of all values in `shape`.

A 0-dimensional array (a single scalar wrapped as an ndarray) has shape `()`, `ndim = 0`, `size = 1` — an empty shape tuple means "no dimensions," not "no data."

## Explanation

`describe_shape` reads `arr.shape`, `arr.ndim`, `arr.size` directly into a dict. `is_shape_valid_for_size` multiplies every entry in `shape` together (`math.prod(shape)`, or an equivalent manual product for an empty tuple, which correctly yields `1`) and compares to `total_elements`.
