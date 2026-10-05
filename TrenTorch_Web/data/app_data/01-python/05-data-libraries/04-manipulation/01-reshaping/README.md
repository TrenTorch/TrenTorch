---
name: numpy-reshaping
title: 'Reshaping & Flattening'
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions that change an array's shape, showing when the result is a view and when it is a copy and that collapse a multi-dimensional array into 1D, demonstrating the key differences between the two ways of doing so.

## Theory

### Changing shape

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

### Flattening

Both `flatten()` and `ravel()` collapse a multi-dimensional array into 1D, in the same row-by-row order. The difference is entirely view versus copy.

**`ravel()` returns a view whenever possible**, it's really `reshape(-1)` under the hood.

```python
arr = np.array([[1, 2], [3, 4]])
r = arr.ravel()
np.shares_memory(arr, r)     # True, typically
```

**`flatten()` always returns a copy, unconditionally.**

```python
f = arr.flatten()
np.shares_memory(arr, f)     # False, always
```

`flatten()` is the safer default when the result will be modified without wanting that to affect the original. `ravel()` avoids an unnecessary copy when that's not a concern.

## Explanation

`reshape_to` and `reshape_with_inferred_dim` are direct `.reshape()` calls (the latter passing `(-1, known_dim)`). `reshape_shares_memory` performs the reshape and checks `np.shares_memory(result, arr)` directly rather than assuming the typical view case always applies.

`flatten_safe` calls `.flatten()`. `flatten_efficient` calls `.ravel()`. `compare_flatten_ravel` computes both and reports each one's `np.shares_memory()` result against `arr` directly, checking the actual outcome rather than assuming, since `ravel()`'s behavior depends on layout even though `flatten()`'s is unconditional.
