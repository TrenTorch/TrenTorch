---
name: systems-perf-quantize-weight-matrix-tradeoff
title: Quantize a Full Weight Matrix, Measure Size/Accuracy Tradeoff
tags: [mlops, neural-networks, quantization]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`01`/`02` built quantize and dequantize as isolated operations. The actual reason anyone quantizes a real model is a tradeoff: smaller storage and faster integer arithmetic, in exchange for some amount of accuracy loss — and "some amount" needs to be an actual measured number, not just an assumption, before shipping a quantized model.

### From theory to code

Implement `quantize_weight_matrix(weight)`, which quantizes a whole weight matrix with one shared `scale`/`zero_point`, then reports both sides of the tradeoff: the compression ratio achieved, and the reconstruction error that compression cost.

### Constraints

- `weight`: any-shape float32 array (e.g. a real layer's weight matrix).
- Returns a dict with `quantized`, `scale`, `zero_point`, `compression_ratio`, `max_abs_error`, `mean_abs_error`.
- `compression_ratio` assumes the original was stored as `float32` (4 bytes/element) and the quantized version as `int8` (1 byte/element) — always exactly `4.0` for this dtype pair, regardless of the matrix's actual values.
- `max_abs_error`/`mean_abs_error`: plain Python floats, computed against the dequantized reconstruction.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

This is almost entirely composition: call `01`'s `quantize` and `02`'s `dequantize`, and this question's own job is just computing and packaging the tradeoff numbers around them.

</details>

<details>
<summary>Hint 2</summary>

`compression_ratio` doesn't depend on the matrix's actual content at all — it's a fixed `4.0` from `4 bytes / 1 byte`, the same for every `float32`-to-`int8` quantization regardless of shape or values.

</details>

## Theory

### The simple version

Quantizing a weight matrix is a trade: pay in accuracy, get paid in size and speed. `01`/`02` already built the mechanics of that trade (the actual mapping and its inverse); this question is about actually pricing it — measuring exactly how much accuracy was spent, and exactly how much size was saved, so that trade can be judged rather than assumed.

### The formula

```text
q, scale, zero_point = quantize(weight)
reconstructed         = dequantize(q, scale, zero_point)

compression_ratio = (weight.size * 4) / (q.size * 1)     # float32 bytes / int8 bytes = 4.0 always
max_abs_error      = max(|weight - reconstructed|)
mean_abs_error     = mean(|weight - reconstructed|)
```

### How PyTorch actually implements this

Context only, untested by your submission: PyTorch's own post-training static quantization workflow (`torch.ao.quantization`) does exactly this — quantize a model's weights (and often activations) to `int8`, then evaluate the quantized model's accuracy against the original to confirm the tradeoff is acceptable before deploying it. Real Linear layers are typically initialized with weights in a narrow, known range (`torch.nn.Linear`'s default Kaiming-uniform init draws from roughly `[-1/sqrt(fan_in), 1/sqrt(fan_in)]`), which is exactly why `int8` quantization tends to cost so little accuracy in practice: the weights' actual range is small and well-behaved, so 256 integer steps across that narrow range still resolve individual weights quite finely.

## Explanation

`quantize_weight_matrix` calls `quantize(weight)` to get `(q, scale, zero_point)`, then `dequantize(q, scale, zero_point)` to reconstruct an approximation of the original matrix. `compression_ratio` compares `weight.size * 4` (the byte cost if every element were stored as `float32`) against `q.size * 1` (the byte cost of the actual `int8` array) — since both counts are the same `weight.size`, this ratio is always exactly `4.0`, independent of the matrix's shape or values. `max_abs_error` and `mean_abs_error` are the worst-case and average per-element gap between `weight` and `reconstructed`, `float(...)`-cast from NumPy's own reduction results so the returned dict holds plain Python numbers rather than 0-d NumPy arrays.
