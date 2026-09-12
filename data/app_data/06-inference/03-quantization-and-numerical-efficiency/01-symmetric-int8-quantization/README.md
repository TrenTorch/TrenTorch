---
name: inf-quant-int8-symmetric
title: 'Symmetric INT8 Quantization'
tags: [inference, quantization, int8]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Storing and computing with 32-bit floats is expensive at inference time — most of that precision is unnecessary for a model that's already trained. Implement symmetric (zero-point-free) INT8 quantization and dequantization for a single tensor: find a scale that maps the tensor's largest-magnitude value to the INT8 range, quantize, and reconstruct an approximation.

### From theory to code

```
scale = max(|x|) / 127
q = clip(round(x / scale), -127, 127)
x_hat = q * scale
```

### Constraints

- `scale = max(abs(x)) / 127`, with `scale = 0` handled explicitly when the tensor is all zeros.
- Quantized values are clipped to the inclusive range `[-127, 127]` as integers.
- Dequantized reconstruction is `q * scale`.
- Return the quantized integer tensor, the scale used, and the dequantized reconstruction.

### Hints

<details>
<summary>Hint: All-zero tensors and rounding order</summary>

Guard against an all-zero tensor: if `max|x|` is 0, scale should be treated as 0 and every quantized value is 0, avoiding a division by zero. Round-then-clip, in that order — clipping before rounding can shift a borderline value across the boundary incorrectly.

</details>

## Theory

### The simple version

Imagine compressing a photo's color palette down to only 255 shades instead of millions — you pick the brightest pixel as your reference point, and every other pixel's brightness is expressed as a fraction of that reference, rounded to the nearest of the 255 available shades.

### The formula

```
scale = max(|x|) / 127
q = clip(round(x / scale), -127, 127)
x_hat = q * scale
```

127 (rather than 128) is used so the representable range is exactly symmetric around 0, avoiding a representational bias toward negative numbers. Because there is no zero-point offset, `0.0` in floating point always maps to exactly `0` in INT8. The **quantization error** `x - x_hat` is bounded by half the step size `scale/2`, which is why choosing scale from the true max keeps error proportional to the tensor's own dynamic range instead of clipping outliers.

### How PyTorch actually implements this

```python
def solve(x):
    import torch
    max_abs = x.abs().max().item() if x.numel() > 0 else 0.0
    scale = max_abs / 127.0 if max_abs > 0 else 0.0
    q = torch.zeros_like(x, dtype=torch.int32) if scale == 0 else torch.clamp(torch.round(x / scale), -127, 127).to(torch.int32)
    return q, scale, q.float() * scale
```

`torch.quantize_per_tensor` implements a related (affine, not purely symmetric) scheme; the symmetric version here maps directly onto how weight-only quantization for linear layers usually works.

## Explanation

Dividing by `scale = max(|x|)/127` maps the largest-magnitude value in `x` to exactly ±127 (the edge of the INT8 range) and every other value proportionally inside it, so rounding to the nearest integer introduces an error no larger than half of one quantization step (`scale/2`) anywhere in the tensor. This is why symmetric quantization's error scales with the tensor's OWN dynamic range rather than a fixed constant: a tensor with small values gets a small `scale` and correspondingly small absolute error, while a tensor with one huge outlier gets a large `scale`, which is exactly the failure mode `[02-per-channel-weight-quantization]` addresses by giving each row its own scale instead of sharing one across a whole matrix.
