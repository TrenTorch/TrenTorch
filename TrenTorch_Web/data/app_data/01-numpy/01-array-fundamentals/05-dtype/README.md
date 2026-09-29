---
name: numpy-dtype
title: dtype
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions that inspect, set, and convert an array's dtype, and observe the consequences of dtype choice.

## Theory

Every ndarray has a single `dtype` describing what type every element in its buffer is — a direct consequence of the buffer being one contiguous block with no per-element type tag. Common dtypes: `int64`/`int32` (signed integers of different bit-widths), `float64`/`float32` (floats of different precision), `bool`.

```python
np.array([1, 2, 3]).dtype     # int64
np.array([1.0, 2.0]).dtype    # float64
```

NumPy infers dtype from the given values, but it can be overridden explicitly:

```python
np.array([1, 2, 3], dtype=np.float32)   # forces float32
```

**Converting dtype** is done with `.astype()`, which returns a **new** array — it never modifies the original in place, since reinterpreting into a differently-sized representation cannot happen inside the original fixed-size buffer.

```python
np.array([1.7, 2.3, 3.9]).astype(np.int64)   # [1, 2, 3] — truncates, does not round
```

Converting float to int **truncates** the decimal part; `1.9` becomes `1`, not `2`.

## Explanation

`get_dtype_name` returns `str(arr.dtype)`. `create_with_dtype` passes `dtype=dtype` straight to `np.array()`. `convert_dtype` calls `arr.astype(new_dtype)` and returns the new array, leaving `arr` untouched — `.astype()` never mutates its receiver.
