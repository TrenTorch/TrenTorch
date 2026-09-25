---
name: numpy-strides
title: Strides
tags: [numpy-memory]
difficulty: Intermediate
---

## Statement

Implement functions that compute an array's strides from its shape and itemsize, use strides to find the byte position of any element, and predict how slicing changes strides without copying data.

## Theory

**Strides** are a tuple with one number per axis, giving how many bytes to move in the buffer to step by one along that axis. Available as `arr.strides`.

```python
arr = np.arange(12, dtype=np.int64).reshape(3, 4)
arr.strides     # (32, 8)
```

The byte offset of element $(i_0, \dots, i_{n-1})$ is:

$$\text{offset} = \sum_{k} i_k \cdot s_k$$

For a C-order array, $s_k = \text{itemsize} \cdot \prod_{j>k} d_j$ — the last axis always has stride equal to the itemsize.

**Views are just different strides.** Slicing along axis 0 with a step rescales only that axis's stride:

```
arr             shape (3, 4)  strides (32, 8)
arr[::2]        shape (2, 4)  strides (64, 8)
arr[::-1]       shape (3, 4)  strides (-32, 8)
```

## Explanation

`compute_c_strides` builds the tuple from the right: start with `itemsize` for the last axis, then repeatedly multiply by the previous dimension size, without ever constructing an array. `byte_offset` is `sum(i * s for i, s in zip(index, strides))`. `slice_step_strides` returns `(arr.strides[0] * step,) + arr.strides[1:]` — only axis 0's stride is rescaled by `step`, every other axis is untouched.
