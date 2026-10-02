---
name: numpy-flatten-vs-ravel
title: flatten vs ravel
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions using both `flatten` and `ravel` to collapse a multi-dimensional array into 1D, and a function that demonstrates their key difference directly.

## Theory

Both `flatten()` and `ravel()` collapse a multi-dimensional array into 1D, in the same row-by-row order. The difference is entirely view versus copy.

**`ravel()` returns a view whenever possible** — it's really `reshape(-1)` under the hood.

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

`flatten_safe` calls `.flatten()`. `flatten_efficient` calls `.ravel()`. `compare_flatten_ravel` computes both and reports each one's `np.shares_memory()` result against `arr` directly — checking the actual outcome rather than assuming, since `ravel()`'s behavior depends on layout even though `flatten()`'s is unconditional.
