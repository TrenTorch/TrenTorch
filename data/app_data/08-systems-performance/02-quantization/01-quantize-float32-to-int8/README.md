---
name: systems-perf-quantize-float32-to-int8
title: Float32 to Int8 Mapping (Quantize)
tags: [mlops, neural-networks, quantization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`03-memory-footprint-estimation` showed that `int8` storage costs a quarter of `float32`'s. Getting there requires actually mapping real-valued numbers onto the 256 discrete integers `int8` can hold — not by truncating decimals (that would throw away almost all the useful range), but by finding an affine transformation that uses the _entire_ integer range for whatever the data's own range actually is.

### From theory to code

Implement `compute_scale_zero_point(x, num_bits=8)`, which finds the one `scale` and one `zero_point` that map `x`'s actual `[min, max]` onto the integer type's full representable range, and `quantize(x, num_bits=8)`, which applies that mapping and rounds to the nearest integer.

### Constraints

- `num_bits=8` means the target range is `[-128, 127]` (signed `int8`).
- `scale`: a positive float, the size of one integer "step" in the original float units.
- `zero_point`: an integer in the target range, the integer value that represents float `0.0`.
- A constant input array (`x.max() == x.min()`) must not divide by zero — fall back to `scale=1.0`.
- `quantize` returns `(q, scale, zero_point)`, `q` as `np.int8`, values always clipped into the valid range even after rounding.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`scale = (x.max() - x.min()) / (qmax - qmin)` — the float range divided by the integer range gives exactly the size of one integer step.

</details>

<details>
<summary>Hint 2</summary>

Once `scale` is known, `x.min()` in float units should land exactly on `qmin` in integer units: `zero_point = round(qmin - x.min() / scale)`, clipped into range in case of rounding at the boundary.

</details>

## Theory

### The simple version

Think of `scale` and `zero_point` as a ruler being redrawn: the float axis's `[min, max]` range gets stretched or compressed to line up exactly with the integer axis's fixed `[-128, 127]` range, and `zero_point` marks where float `0.0` lands on that new integer ruler (which usually isn't the integer `0`, unless the float data happens to be centered exactly there). Every float value then reads off wherever it falls on this newly-calibrated integer ruler.

### The formula

```text
qmin, qmax = -128, 127                                    # for num_bits=8
scale      = (x.max() - x.min()) / (qmax - qmin)
zero_point = round(qmin - x.min() / scale), clipped to [qmin, qmax]

quantize(x) = clip(round(x / scale + zero_point), qmin, qmax)
```

### How PyTorch actually implements this

`torch.quantize_per_tensor(x, scale, zero_point, dtype=torch.qint8)` performs exactly this affine mapping given a `scale`/`zero_point` — verified directly in this exercise's own `tests.py`, whose `test_10_matches_real_pytorch_quantize_per_tensor_on_a_baked_reference_case` bakes in an `int8` array generated once, offline, by calling `torch.quantize_per_tensor` with the _exact_ `scale`/`zero_point` this exercise's own `compute_scale_zero_point` produces — confirming the formula above is not just "a" quantization scheme, but the same one PyTorch's quantization tooling actually implements. Real deployments typically compute `scale`/`zero_point` once, offline, by observing a representative calibration dataset's range (rather than per-inference on live data), then bake those fixed values into the deployed, quantized model.

## Explanation

`compute_scale_zero_point` computes `qmin`/`qmax` from `num_bits`, then `scale` as the float range divided by the integer range — guarded against `x_max == x_min` (a constant array) by falling back to `scale=1.0`, since dividing by a zero range would otherwise produce `inf`/`nan`. `zero_point` is computed by asking "what integer does `x`'s own minimum map to, given this scale," then rounding and clipping the result into `[qmin, qmax]` in case floating-point rounding pushes it just outside.

`quantize` reuses `compute_scale_zero_point`, then applies the forward mapping `x / scale + zero_point` (converting float units into integer units), rounds to the nearest whole number, clips into range one more time (protecting against any single value that happened to fall slightly outside due to rounding), and casts to `np.int8` — the actual, storable, quarter-the-size representation `03-memory-footprint-estimation` promised.
