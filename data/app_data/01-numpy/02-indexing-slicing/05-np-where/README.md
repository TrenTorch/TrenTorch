---
name: numpy-np-where
title: np.where
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions using `np.where` both to find the positions satisfying a condition and to build a new array by choosing between two values based on a condition.

## Theory

**One-argument form: `np.where(condition)`** returns the indices where `condition` is `True`, as a tuple (one array per dimension).

```python
arr = np.array([5, 12, 3, 18, 7])
np.where(arr > 10)      # (array([1, 3]),)
```

**Three-argument form: `np.where(condition, if_true_value, if_false_value)`** builds a new array of the same shape as `condition`, choosing `if_true_value` where `True` and `if_false_value` where `False`. Either value can be a scalar or an array of matching shape.

```python
arr = np.array([5, 12, 3, 18, 7])
np.where(arr > 10, 1, 0)      # [0, 1, 0, 1, 0]
np.where(arr > 10, arr, -1)   # [-1, 12, -1, 18, -1]
```

This is a vectorized replacement for an `if/else` inside a loop over every element.

## Explanation

`find_indices_above` uses the one-argument form and takes index `[0]` of the returned tuple, since `arr` is guaranteed 1D. `replace_above_threshold` and `sign_labels` use the three-argument form directly — `sign_labels` passes the string values `"positive"`/`"non-positive"` as the two branches, which NumPy broadcasts across the whole array without a loop.
