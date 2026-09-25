---
name: numpy-creating-arrays-from-python-data
title: Creating Arrays From Python Data
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement functions that convert Python lists and nested lists into ndarrays using `np.array()`, and observe how nesting depth becomes array dimensionality.

## Theory

`np.array()` takes a Python list (or nested list) and **copies** its values into a new, contiguous buffer — it does not reuse the original list's storage, since a list's storage (scattered pointers) isn't even the same kind of layout an ndarray uses.

**Nested lists become multi-dimensional arrays.** A list of lists, where every inner list has the same length, becomes a 2-dimensional array — the outer list's length becomes the first dimension, each inner list's length becomes the second:

```python
np.array([[1, 2, 3], [4, 5, 6]])   # shape (2, 3)
```

This nests further: a list of lists of lists becomes 3-dimensional, and so on. Every inner list at a given nesting depth must have the same length, or `np.array()` cannot determine a consistent shape.

`np.array()` also accepts an explicit `dtype` argument to override what it would otherwise infer.

## Explanation

Both functions are one-line calls to `np.array()` — the whole point of this topic is that `np.array()` already does the dimension inference from nesting depth automatically, so no manual shape computation or loop is needed for either the flat or nested case. The hidden tests' "does not share memory with the original list" check passes for free here too, since `np.array()` always copies regardless of how it's called.
