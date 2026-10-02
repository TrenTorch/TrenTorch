---
name: numpy-tensor-shape-dtype-device
title: 'From ndarray to Tensor: Shape, Dtype, and Device'
tags: [numpy-tensors]
difficulty: Beginner
---

## Statement

Implement functions that model a tensor's metadata on top of an ndarray — shape, dtype, and the new `device` field — and apply the two tensor-specific rules that differ from NumPy's defaults.

## Theory

A PyTorch **tensor** is the same kind of object as an ndarray: a small metadata object describing one contiguous buffer. Everything from Module 1 carries over — `shape`, `dtype`, strides. A tensor adds one new field: **`device`**, the processor whose memory holds the buffer (`"cpu"` or `"cuda"`).

Two consequences:

1. **An operation between two tensors requires both to be on the same device** — mixing devices raises an error rather than converting silently.
2. **Moving a tensor to a different device is always a copy** — different physical memory means the bytes must be transferred.

Two practical differences from NumPy's defaults:

- **Default float dtype.** NumPy creates floats as `float64`; tensors created from Python floats default to `float32`.
- **Sharing with NumPy.** A CPU tensor can be created from an ndarray describing the _same buffer_ — the Module 3 view model applied across libraries.

## Explanation

`make_tensor_meta` returns `{"shape": arr.shape, "dtype": str(arr.dtype), "device": device}`. `cast_floats_to_tensor_default` checks `arr.dtype == np.float64` and returns `arr.astype(np.float32)` if so, else `arr` unchanged — `.astype()` always returns a new array when the dtype actually changes, so `arr` itself is never mutated. `check_same_device` compares the two strings and raises `ValueError(f"...{device_a}...{device_b}...")` on mismatch, returning `None` otherwise.
