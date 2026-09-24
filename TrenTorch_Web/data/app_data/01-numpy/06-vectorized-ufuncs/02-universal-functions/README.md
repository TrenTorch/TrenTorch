---
name: numpy-universal-functions
title: Universal Functions (ufuncs)
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement functions using common universal functions like `np.sqrt`, `np.exp`, `np.log`, and `np.abs`.

## Theory

A **universal function**, or **ufunc**, operates element-wise across an entire array in a single call — the arithmetic operators themselves are implemented as ufuncs internally.

```python
np.sqrt(np.array([1.0, 4.0, 9.0]))     # [1.0, 2.0, 3.0]
np.exp(np.array([0.0, 1.0, 2.0]))       # [1.0, 2.718..., 7.389...]
np.log(np.array([1.0, 2.718..., 7.389...]))   # inverse of exp
```

Common ufuncs: `np.sqrt`, `np.exp`, `np.log`, `np.sin`/`np.cos`/`np.tan`, `np.abs`, and more, all applying their single-input operation to every element independently, returning a new array of the same shape.

Some ufuncs take two arrays — `np.add`, `np.multiply`, `np.power` are the actual ufuncs underlying `+`, `*`, `**`.

## Explanation

Each function is a direct call to the matching ufunc: `np.sqrt(arr)`, `np.exp(arr)`, `np.log(arr)`, `np.abs(arr)`. Every one preserves the input's shape, since a ufunc always produces one output value per input element.
