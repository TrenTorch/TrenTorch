---
name: numpy-tensor-views-broadcasting-vectorization
title: 'Everything Carries Over: Views, Broadcasting, Vectorization'
tags: [numpy-tensors]
difficulty: Intermediate
---

## Statement

Implement functions that use the views/copies test, the broadcasting rule, and vectorized column-wise arithmetic — the three mental models from this track — in forms that apply identically to tensors.

## Theory

**Views and copies.** A basic slice, transpose, and contiguous reshape are views; fancy indexing, boolean masking, and arithmetic produce new buffers. The reliable test: do the two objects share memory (`np.shares_memory`)?

**Broadcasting.** Unchanged: align from the trailing axis, compatible if equal or one is `1`.

$$r_i = \begin{cases} d_i & \text{if } d_i = e_i \text{ or } e_i = 1 \\ e_i & \text{if } d_i = 1 \\ \text{error} & \text{otherwise} \end{cases}$$

**Vectorization.** Operating on whole tensors rather than looping is even more important on a GPU.

**Same concepts, different spellings:** `axis=` → `dim=`, `np.expand_dims`/`newaxis` → `unsqueeze`, `.astype(dtype)` → `.to(dtype)`, `np.ascontiguousarray` → `.contiguous()`.

## Explanation

`predict_broadcast_shape` pads the shorter shape with leading `1`s, walks pairs from the right, raising `ValueError` the moment a pair is neither equal nor has a `1` (same logic as Module 5's rule, implemented directly rather than via `np.broadcast_shapes`). `classify_by_memory` calls `op(arr)` and checks `np.shares_memory(op(arr), arr)`. `standardize_columns` computes `arr.mean(axis=0)` and `arr.std(axis=0)`, then `(arr - col_mean) / (col_std + eps)` — the `+ eps` in the denominator keeps a zero-variance column from dividing by exactly zero, giving `0 / eps == 0` instead of `NaN`.
