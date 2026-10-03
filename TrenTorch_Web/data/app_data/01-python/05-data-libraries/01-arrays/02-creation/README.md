---
name: numpy-array-creation
title: Creating Arrays
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement functions that convert Python lists and nested lists into arrays, observing how nesting depth becomes array dimension and that create arrays of a specified shape without manually listing every value.

## Theory

### From Python data

`np.array()` takes a Python list (or nested list) and **copies** its values into a new, contiguous buffer, it does not reuse the original list's storage, since a list's storage (scattered pointers) isn't even the same kind of layout an ndarray uses.

**Nested lists become multi-dimensional arrays.** A list of lists, where every inner list has the same length, becomes a 2-dimensional array, the outer list's length becomes the first dimension, each inner list's length becomes the second:

```python
np.array([[1, 2, 3], [4, 5, 6]])   # shape (2, 3)
```

This nests further: a list of lists of lists becomes 3-dimensional, and so on. Every inner list at a given nesting depth must have the same length, or `np.array()` cannot determine a consistent shape.

`np.array()` also accepts an explicit `dtype` argument to override what it would otherwise infer.

### Filled arrays

`np.zeros(shape)` creates an array of the given shape filled entirely with `0`. `np.ones(shape)` fills entirely with `1`. `np.full(shape, fill_value)` fills entirely with `fill_value`. `shape` is a tuple giving the size of each dimension, `(2, 3)` means 2 rows, 3 columns.

```python
np.zeros((2, 3))      # 2x3 array, every element 0
np.full((2, 2), 7)     # 2x2 array, every element 7
```

`np.empty(shape)` also allocates an array of the given shape but does not initialize its values, the buffer contains whatever bytes were already there. It is faster than `zeros`/`ones` only when every element will be immediately overwritten, and should never be used when predictable starting values are needed.

All these functions default to a floating-point dtype unless a `dtype` argument is given, even when the fill value looks like an integer.

## Explanation

Both functions are one-line calls to `np.array()`, the whole point of this topic is that `np.array()` already does the dimension inference from nesting depth automatically, so no manual shape computation or loop is needed for either the flat or nested case. The hidden tests' "does not share memory with the original list" check passes for free here too, since `np.array()` always copies regardless of how it's called.

Each function is a direct, one-line call to the matching NumPy generator, passing `(rows, cols)` as the shape tuple. No manual value-by-value construction is needed, that is the entire point of these generators existing.
