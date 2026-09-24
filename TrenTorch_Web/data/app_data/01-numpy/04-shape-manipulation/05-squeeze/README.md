---
name: numpy-squeeze
title: squeeze
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement functions that remove size-1 dimensions from an array, the inverse operation of `newaxis`/`expand_dims`.

## Theory

`squeeze()` removes dimensions of size 1 from an array's shape, without changing its values or its total `size`.

```python
arr = np.zeros((1, 3, 1, 4))
arr.squeeze().shape     # (3, 4) — both size-1 dimensions removed
```

Called with no arguments, it removes every size-1 dimension. An explicit `axis` argument restricts this to a specific dimension, and raises an error if that dimension isn't actually size 1:

```python
arr.squeeze(axis=0).shape     # (3, 1, 4) — only axis 0 removed
arr.squeeze(axis=1)             # raises — axis 1 has size 3, not 1
```

Like `newaxis`/`expand_dims`, `squeeze()` never changes the total element count, so it follows the same view-returning behavior as the rest of this module's reshaping-family operations.

## Explanation

`remove_all_singleton_dims` calls `arr.squeeze()`. `remove_singleton_at` calls `arr.squeeze(axis=axis)`. Both are direct, unconditional calls — the axis-safety check (raising when a non-size-1 axis is targeted) is handled entirely by NumPy itself.
