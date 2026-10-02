---
name: numpy-assemble-memory-layout-audit
title: 'Assemble: Memory-Layout Audit of an Array'
tags: [numpy-memory]
difficulty: Advanced
---

## Statement

Implement one function that inspects a 2D array's strides, contiguity, and reshape behavior, produces a contiguous version, and measures loop vs vectorized summation.

## Theory

This problem introduces no new concepts. It combines every topic in this module:

- Use strides and `nbytes` to describe how the array is laid out, and compute what strides a C-contiguous array of the same shape would have.
- Read the contiguity flag.
- Determine whether a reshape would silently copy, and produce a contiguous version with a copy only when one is needed.
- Measure the speedup of a vectorized sum over a nested Python loop.

A C-contiguous array's strides always equal the expected C-order strides for its shape, so comparing `strides` against `expected_c_strides` is a second way to reach the same conclusion as the `C_CONTIGUOUS` flag for arrays with no size-1 dimensions.

## Explanation

`expected_c_strides` is computed from `arr.shape` and `arr.itemsize` directly (the same C-order formula as the strides topic), never read off `arr.strides`. `reshape_copies` and `conversion_copied` both use `np.shares_memory`. `contiguous_version` is `np.ascontiguousarray(arr)`. The nested-loop total accumulates `for row in arr: for value in row: total += value`, timed with `best_time`-style repeated measurement against `arr.sum()`, and compared with `np.isclose`.
