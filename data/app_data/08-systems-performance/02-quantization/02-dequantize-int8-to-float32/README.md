---
name: systems-perf-dequantize-int8-to-float32
title: Int8 to Float32 Reconstruction (Dequantize)
tags: [mlops, neural-networks, quantization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Storing weights as `int8` is only useful if they can be turned back into something a floating-point computation can actually use. `01-quantize-float32-to-int8`'s `scale`/`zero_point` are exactly the two numbers needed to invert that mapping — but the inversion is necessarily lossy: rounding to the nearest integer during quantization permanently discards whatever fraction of a "step" the true value didn't land exactly on.

### From theory to code

Implement `dequantize(q, scale, zero_point)`, which inverts `quantize`'s forward mapping, and `quantization_error(x, q, scale, zero_point)`, which measures how much information that round trip actually lost.

### Constraints

- `dequantize(q, scale, zero_point)` returns a float array the same shape as `q`.
- `quantization_error` returns a single float: the maximum absolute difference between the original values and their reconstruction.
- Casting `q` to a floating-point dtype must happen _before_ subtracting `zero_point` — subtracting first, while still an `int8` array, can silently wrap around on overflow.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`quantize`'s forward mapping was `x / scale + zero_point`. Inverting an "divide then add" is "subtract then multiply": `(q - zero_point) * scale`.

</details>

<details>
<summary>Hint 2</summary>

`q.astype(np.float32)` before doing any arithmetic on it avoids int8's wraparound overflow — `np.int8(-128) - 100` wraps to a wrong, small positive number if computed in int8, but the correct large negative number once cast to float first.

</details>

## Theory

### The simple version

If quantizing was redrawing the ruler from float units to integer units, dequantizing is reading that same ruler backward: given an integer position, multiply by the step size (`scale`) and shift back by however far `zero_point` had moved things, to recover (approximately) where that value sat on the original float ruler. "Approximately" is the key word — quantization rounded to the nearest integer step, so dequantizing can only ever return the _center_ of whichever step the original value happened to round into, not the original value's exact position within that step.

### The formula

```text
dequantize(q, scale, zero_point) = (q - zero_point) * scale
quantization_error(x, q, scale, zero_point) = max(|x - dequantize(q, scale, zero_point)|)
```

Since rounding can shift a value by at most half an integer step in either direction, the worst-case error for any single value is bounded by `scale / 2` — a smaller `scale` (a finer-grained integer ruler) always means a smaller worst-case reconstruction error, at the cost of the integer range covering a narrower span of float values for the same bit width.

### How PyTorch actually implements this

`QTensor.dequantize()` (the method on any tensor produced by `torch.quantize_per_tensor`) performs exactly this affine inverse — verified directly in this exercise's own `tests.py`, whose `test_10_matches_real_pytorch_dequantize_on_a_baked_reference_case` bakes in float values generated once, offline, from a real, quantized PyTorch tensor's own `.dequantize()` call. A real quantized model runs its actual matrix multiplications in integer arithmetic for speed, and only dequantizes back to float where a downstream operation genuinely needs floating-point precision (e.g. a softmax).

## Explanation

`dequantize` casts `q` to `np.float32` first (avoiding `int8`'s overflow-wraparound entirely, since the subtraction and multiplication both now happen in float arithmetic), subtracts `zero_point` (undoing the shift that made float `0.0` land on a specific integer), and multiplies by `scale` (converting integer "step count" back into float units) — the exact algebraic inverse of `quantize`'s `x / scale + zero_point` forward mapping.

`quantization_error` calls `dequantize` to reconstruct the original array as closely as quantization allowed, then returns `np.max(np.abs(x - reconstructed))` — the single largest per-element gap between the true and reconstructed values, a direct, honest measure of how much precision the round trip through `int8` actually cost.
