---
name: numpy-conditional-selection
title: Conditional Selection
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions that build boolean condition arrays and use them to select and modify elements without an explicit loop, find the positions satisfying a condition and build a new array by choosing between two values based on a condition.

## Theory

### Boolean masks

Applying a comparison operator to an entire array produces a new same-shape array of `True`/`False` values, one per element, a **mask**.

```python
arr = np.array([10, 15, 20, 25, 30])
mask = arr > 18       # [False, False, True, True, True]
arr[mask]              # [20, 25, 30]
```

Multiple conditions combine with `&`, `|`, `~`, **not** Python's `and`/`or`/`not`, which only work on single booleans. Each combined condition needs parentheses:

```python
arr[(arr > 10) & (arr < 25)]     # strictly between 10 and 25
```

Boolean masking can also assign, updating only selected elements in place:

```python
arr[arr > 18] = 0
```

Unlike slicing, reading through a mask (`arr[mask]`) always returns a **copy**, since the selected elements are scattered and can't be described as "a start position and a step."

### Positions & conditional values

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

`select_above_threshold` and `select_in_range` build the mask inline and index with it (`arr[arr > threshold]`, `arr[(arr > low) & (arr < high)]`), each returns a new copied array. `zero_out_negatives` assigns through the mask (`arr[arr < 0] = 0`) directly on the parameter, mutating in place with no reassignment.

`find_indices_above` uses the one-argument form and takes index `[0]` of the returned tuple, since `arr` is guaranteed 1D. `replace_above_threshold` and `sign_labels` use the three-argument form directly, `sign_labels` passes the string values `"positive"`/`"non-positive"` as the two branches, which NumPy broadcasts across the whole array without a loop.
