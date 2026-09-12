---
name: inf-quant-per-channel
title: 'Per-Channel Weight Quantization for Linear Layers'
tags: [inference, quantization, int8, per-channel]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[01-symmetric-int8-quantization]`'s single global scale for an entire weight matrix is dominated by whichever row happens to have the largest values — every OTHER row is then quantized far more coarsely than it needs to be, wasting precision. Implement per-channel (per-output-row) symmetric INT8 quantization for a weight matrix: instead of one global scale for the whole matrix, compute an independent scale for each output channel (row).

### From theory to code

```
scale[o] = max(|W[o, :]|) / 127     for each output channel o
Q[o, :] = clip(round(W[o, :] / scale[o]), -127, 127)
```

### Constraints

- One independent scale per output row (axis=0 of the weight matrix), computed exactly as in symmetric per-tensor quantization but restricted to that row.
- Rows with all-zero weights get scale 0 and an all-zero quantized row.
- Return the quantized integer matrix, the per-row scale vector, and the dequantized reconstruction.

### Hints

<details>
<summary>Hint: Vectorize over rows, don't loop</summary>

Compute `np.max(np.abs(W), axis=1)` to get one max-abs value per row in a single vectorized call. Broadcast each row's scale over its own row when quantizing: `W / scale[:, None]`, not `W / scale`.

</details>

## Theory

### The simple version

Instead of grading an entire class on one curve set by the single hardest question on the exam (crushing everyone's other answers' apparent quality), grade each QUESTION on its own curve — every question gets scored relative to its own range of answers.

### The formula

```
scale[o] = max(|W[o,:]|) / 127   for each row o
Q[o,:] = clip(round(W[o,:] / scale[o]), -127, 127)
```

A linear layer's output channels are computed independently (`y[o] = W[o,:] . x`), so each row can be quantized with its own scale without any extra cost at inference time: dequantizing simply multiplies each output channel by its own scale after the INT8 matmul, exactly the per-channel scaling factor already applied elementwise.

### How PyTorch actually implements this

```python
def solve(W):
    import torch
    max_abs = W.abs().max(dim=1).values
    scale = torch.where(max_abs > 0, max_abs / 127.0, torch.zeros_like(max_abs))
    safe_scale = torch.where(scale == 0, torch.ones_like(scale), scale)
    Q = torch.clamp(torch.round(W / safe_scale[:, None]), -127, 127)
    Q = torch.where((scale == 0)[:, None], torch.zeros_like(Q), Q).to(torch.int32)
    return Q, scale, Q.float() * scale[:, None]
```

Per-channel quantization is the standard choice for weights precisely because this "one scale per output row" granularity is free to apply at inference (a single extra elementwise multiply per output) but meaningfully reduces quantization error versus one scale for the whole matrix.

## Explanation

Broadcasting `scale[:, None]` applies exactly one scalar per row across that row's `in_features` columns, which is mathematically identical to running the single-tensor symmetric quantization routine independently on each row — but expressed as one vectorized operation instead of a Python loop over rows. This is why per-channel quantization is "free" at inference: since each output channel's dequantization is just multiplying that channel's raw INT8 accumulator by its own scale, the extra cost versus per-tensor quantization is a single elementwise multiply after the matmul, not a fundamentally more expensive operation.
