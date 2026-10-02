---
name: numpy-contiguous-vs-non-contiguous
title: Contiguous vs Non-Contiguous Arrays
tags: [numpy-memory]
difficulty: Intermediate
---

## Statement

Implement functions that read an array's contiguity flags and classify which slicing and transposing operations produce contiguous results and which do not.

## Theory

An array is **C-contiguous** when its elements, read in row-by-row order, sit in the buffer back-to-back with no gaps — equivalently, its strides equal the C-order strides. A freshly created array is C-contiguous. **F-contiguous** is the same idea in column-by-column order.

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

`contiguity_flags` returns `{"c_contiguous": arr.flags["C_CONTIGUOUS"], "f_contiguous": arr.flags["F_CONTIGUOUS"]}` directly. `contiguity_of_ops` performs each of the five listed operations and reads `.flags["C_CONTIGUOUS"]` off each result — the actual flag values are computed by NumPy from the resulting strides, so no manual stride reasoning is needed here.
