---
name: numpy-boolean-masking
title: Boolean Masking
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions that build boolean condition arrays and use them to select and modify elements, without writing an explicit loop over the array.

## Theory

Applying a comparison operator to an entire array produces a new same-shape array of `True`/`False` values, one per element — a **mask**.

```python
arr = np.array([10, 15, 20, 25, 30])
mask = arr > 18       # [False, False, True, True, True]
arr[mask]              # [20, 25, 30]
```

Multiple conditions combine with `&`, `|`, `~` — **not** Python's `and`/`or`/`not`, which only work on single booleans. Each combined condition needs parentheses:

```python
arr[(arr > 10) & (arr < 25)]     # strictly between 10 and 25
```

Boolean masking can also assign, updating only selected elements in place:

```python
arr[arr > 18] = 0
```

Unlike slicing, reading through a mask (`arr[mask]`) always returns a **copy**, since the selected elements are scattered and can't be described as "a start position and a step."

## Explanation

`select_above_threshold` and `select_in_range` build the mask inline and index with it (`arr[arr > threshold]`, `arr[(arr > low) & (arr < high)]`) — each returns a new copied array. `zero_out_negatives` assigns through the mask (`arr[arr < 0] = 0`) directly on the parameter, mutating in place with no reassignment.
