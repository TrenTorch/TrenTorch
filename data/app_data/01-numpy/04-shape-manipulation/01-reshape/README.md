---
name: numpy-reshape
title: reshape
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions that change an array's shape using `reshape`, and a function that demonstrates exactly when reshape can return a view versus when it must return a copy.

## Theory

`reshape` regroups an array's existing buffer into a new shape without changing the values or their order.

```python
arr = np.arange(12)          # shape (12,)
grid = arr.reshape((3, 4))     # same 12 values, now 3 rows of 4
```

The new shape's product must exactly equal the array's existing `size`, or NumPy raises an error. One dimension can be `-1`, telling NumPy to infer it:

```python
np.arange(12).reshape((3, -1))     # infers 4: shape (3, 4)
np.arange(12).reshape((-1, 4))     # infers 3: shape (3, 4)
```

**Whether `reshape` returns a view or a copy** follows Module 3's general rule: since reshape only regroups existing values, it can almost always be a view. It falls back to a copy only when the array's existing memory layout is incompatible with the requested shape (e.g. some non-contiguous results of `transpose`). The reliable way to know which happened is `np.shares_memory()`, not assumption.

## Explanation

`reshape_to` and `reshape_with_inferred_dim` are direct `.reshape()` calls (the latter passing `(-1, known_dim)`). `reshape_shares_memory` performs the reshape and checks `np.shares_memory(result, arr)` directly rather than assuming the typical view case always applies.
