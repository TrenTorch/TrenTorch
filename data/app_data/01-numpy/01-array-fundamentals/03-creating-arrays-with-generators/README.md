---
name: numpy-creating-arrays-with-generators
title: Creating Arrays With Generators
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement functions using `np.zeros`, `np.full`, and `np.ones` to create arrays of a specified shape without manually listing every value.

## Theory

`np.zeros(shape)` creates an array of the given shape filled entirely with `0`. `np.ones(shape)` fills entirely with `1`. `np.full(shape, fill_value)` fills entirely with `fill_value`. `shape` is a tuple giving the size of each dimension — `(2, 3)` means 2 rows, 3 columns.

```python
np.zeros((2, 3))      # 2x3 array, every element 0
np.full((2, 2), 7)     # 2x2 array, every element 7
```

`np.empty(shape)` also allocates an array of the given shape but does not initialize its values — the buffer contains whatever bytes were already there. It is faster than `zeros`/`ones` only when every element will be immediately overwritten, and should never be used when predictable starting values are needed.

All these functions default to a floating-point dtype unless a `dtype` argument is given, even when the fill value looks like an integer.

## Explanation

Each function is a direct, one-line call to the matching NumPy generator, passing `(rows, cols)` as the shape tuple. No manual value-by-value construction is needed — that is the entire point of these generators existing.
