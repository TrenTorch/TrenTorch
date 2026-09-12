---
name: inf-quant-int4-groupwise
title: 'Group-Wise INT4 Weight Quantization (GPTQ/AWQ-style)'
tags: [inference, quantization, int4, group-wise]
difficulty: Advanced
---

## Statement

### The problem, from first principles

INT4 has only 16 representable levels (`-7..7` signed, using symmetric quantization), so a single scale per row (`[02-per-channel-weight-quantization]`'s approach) is often too coarse: any local variation in magnitude within a row gets quantized very lossily. Implement group-wise ("group quantization") INT4 weight quantization: split each row of a weight matrix into fixed-size contiguous groups along the input dimension, and quantize each group with its own independent scale — the scheme used by popular INT4 weight-only quantization methods (GPTQ, AWQ) in production LLM serving.

### From theory to code

```
scale[o, g] = max(|W[o, g*group_size:(g+1)*group_size]|) / 7
Q[o, i] = clip(round(W[o, i] / scale[o, i // group_size]), -7, 7)
```

### Constraints

- `in_features` must be divisible by `group_size`.
- Each contiguous group of `group_size` input features (per row) gets its own scale, computed the same way as symmetric quantization restricted to that group.
- INT4 signed symmetric range is `[-7, 7]`.
- Return the quantized matrix, the `(out_features, n_groups)` scale matrix, and the dequantized reconstruction.

### Hints

<details>
<summary>Hint: Reshape, don't loop over groups</summary>

Reshape each row's `in_features` values into `(n_groups, group_size)` to compute all group scales with one `np.max(np.abs(...), axis=-1)` call instead of a nested Python loop. Assume `in_features` already divides evenly by `group_size` — no ragged final group in this simplified scheme.

</details>

## Theory

### The simple version

Per-channel quantization (`[02-per-channel-weight-quantization]`) already curves each exam question separately. Group-wise quantization goes one step further: curve each SMALL CLUSTER of sub-questions within a question separately too, since even within one row, weight magnitudes can vary a lot from one chunk of input features to another.

### The formula

```
scale[o, g] = max(|W[o, g*group_size:(g+1)*group_size]|) / 7
Q[o, i] = clip(round(W[o, i] / scale[o, i // group_size]), -7, 7)
```

The cost is metadata: instead of 1 scale per row, `in_features / group_size` scales are stored per row. `group_size` is a genuine trade-off knob — smaller groups reduce quantization error but increase the number of stored scale values (and therefore the effective bits-per-weight once metadata is accounted for).

### How PyTorch actually implements this

```python
def solve(W, group_size):
    import torch
    out_features, in_features = W.shape
    n_groups = in_features // group_size
    Wg = W.view(out_features, n_groups, group_size)
    max_abs = Wg.abs().amax(dim=-1)
    scale = torch.where(max_abs > 0, max_abs / 7.0, torch.zeros_like(max_abs))
    safe_scale = torch.where(scale == 0, torch.ones_like(scale), scale)
    Qg = torch.clamp(torch.round(Wg / safe_scale[:, :, None]), -7, 7)
    Qg = torch.where((scale == 0)[:, :, None], torch.zeros_like(Qg), Qg).to(torch.int32)
    W_hat = (Qg.float() * scale[:, :, None]).view(out_features, in_features)
    return Qg.view(out_features, in_features), scale, W_hat
```

GPTQ and AWQ both use group sizes of 32, 64, or 128 in practice — small enough to keep error low, large enough that the scale metadata stays a small fraction of the total model size.

## Explanation

Reshaping `in_features` into `(n_groups, group_size)` turns "quantize each contiguous group independently" into a single axis-wise reduction (`max(abs(.), axis=-1)`) plus a broadcasted division — mathematically the same as looping over groups and quantizing each one separately, just vectorized. This reshape-then-reduce pattern is the same trick used throughout this track (per-channel quantization reduces over columns, block-wise FP8 quantization in `[04-blockwise-fp8-quantization]` reduces over 2D tiles) — the granularity of quantization is entirely a question of which axis (or axes) the max-reduction happens over before broadcasting the resulting scale back out.
