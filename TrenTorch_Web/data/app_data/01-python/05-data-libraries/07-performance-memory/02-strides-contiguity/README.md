---
name: numpy-strides-contiguity
title: 'Strides & Contiguity'
tags: [numpy-memory]
difficulty: Intermediate
---

## Statement

Implement functions that compute an array's strides from its shape and itemsize, use strides to find the byte position of any element and read an array's contiguity flags to classify which slicing and transposing operations keep the layout contiguous.

## Theory

### Strides

**Strides** are a tuple with one number per axis, giving how many bytes to move in the buffer to step by one along that axis. Available as `arr.strides`.

```python
arr = np.arange(12, dtype=np.int64).reshape(3, 4)
arr.strides     # (32, 8)
```

The byte offset of element $(i_0, \dots, i_{n-1})$ is:

$$\text{offset} = \sum_{k} i_k \cdot s_k$$

For a C-order array, $s_k = \text{itemsize} \cdot \prod_{j>k} d_j$, the last axis always has stride equal to the itemsize.

**Views are just different strides.** Slicing along axis 0 with a step rescales only that axis's stride:

```
arr             shape (3, 4)  strides (32, 8)
arr[::2]        shape (2, 4)  strides (64, 8)
arr[::-1]       shape (3, 4)  strides (-32, 8)
```

### Contiguous vs non-contiguous arrays

An array is **C-contiguous** when its elements, read in row-by-row order, sit in the buffer back-to-back with no gaps, equivalently, its strides equal the C-order strides. A freshly created array is C-contiguous. **F-contiguous** is the same idea in column-by-column order.

```python
arr = np.arange(12).reshape(3, 4)
arr.flags["C_CONTIGUOUS"]     # True
arr.flags["F_CONTIGUOUS"]     # False
```

Given a 2D C-contiguous array with strides `(32, 8)`:

| Operation                  | C-contiguous? | Why                                             |
| -------------------------- | ------------- | ----------------------------------------------- |
| `arr[1:3]` (row slice)     | Yes           | A run of whole rows is still one unbroken block |
| `arr[:, 0]` (one column)   | No            | Each element is a whole row apart               |
| `arr[::2]` (every 2nd row) | No            | Whole rows are skipped between kept rows        |
| `arr.T`                    | No            | Strides swapped; F-contiguous instead           |
| `arr.T.copy()`             | Yes           | A copy is written into a fresh C-order buffer   |

A 1D array with stride equal to its itemsize is contiguous in both senses.

## Explanation

`compute_c_strides` builds the tuple from the right: start with `itemsize` for the last axis, then repeatedly multiply by the previous dimension size, without ever constructing an array. `byte_offset` is `sum(i * s for i, s in zip(index, strides))`. `slice_step_strides` returns `(arr.strides[0] * step,) + arr.strides[1:]`, only axis 0's stride is rescaled by `step`, every other axis is untouched.

`contiguity_flags` returns `{"c_contiguous": arr.flags["C_CONTIGUOUS"], "f_contiguous": arr.flags["F_CONTIGUOUS"]}` directly. `contiguity_of_ops` performs each of the five listed operations and reads `.flags["C_CONTIGUOUS"]` off each result, the actual flag values are computed by NumPy from the resulting strides, so no manual stride reasoning is needed here.
