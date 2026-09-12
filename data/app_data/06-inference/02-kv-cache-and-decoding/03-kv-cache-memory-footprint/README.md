---
name: inf-kv-memory-footprint
title: 'KV Cache Memory Footprint Across Attention Variants'
tags: [inference, kv-cache, memory, capacity-planning]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`[02-autoregressive-decoding-kv-cache]` built a cache that grows one row per generated token. Every real serving deployment needs to know, ahead of time, how much GPU memory that cache will actually consume — this is the calculation every serving-capacity plan starts from. Compute the KV cache memory footprint (in bytes) for a batch of sequences, given model shape parameters and which attention variant (MHA, MQA, or GQA) is in use.

### From theory to code

```
kv_heads = n_heads (MHA)  |  1 (MQA)  |  n_kv_heads (GQA)
bytes_per_token = 2 * n_layers * kv_heads * d_head * bytes_per_element
total_bytes = batch_size * seq_len * bytes_per_token
```

### Constraints

- `variant` is one of `'mha'`, `'mqa'`, `'gqa'`; for `'mha'` effective `kv_heads = n_heads`, for `'mqa'` it's `1`, for `'gqa'` it's the given `n_kv_heads`.
- Account for K and V separately (factor of 2).
- Multiply across `n_layers`, `seq_len`, and `batch_size`.
- Return total bytes, and also bytes-per-token-per-layer for reference.

### Hints

<details>
<summary>Hint: A pure product, no loops needed</summary>

The formula is a pure product of six numbers — no loops or matrices needed, just get the variant-to-`kv_heads` mapping right. Always include the factor of 2 for storing both K and V, not just one of them.

</details>

## Theory

### The simple version

Every layer of a transformer needs its own KV cache slot. For each layer, one token contributes `kv_heads * d_head` numbers for K and the same for V, so `2 * kv_heads * d_head` numbers per layer per token. Multiply by `n_layers`, `bytes_per_element` (2 for fp16/bf16, 4 for fp32, 1 for int8), `seq_len`, and `batch_size` to get the total cache size.

### The formula

```
kv_heads = n_heads (MHA) | 1 (MQA) | n_kv_heads (GQA)
bytes_per_token_per_layer = 2 * kv_heads * d_head * bytes_per_element
bytes_per_token = n_layers * bytes_per_token_per_layer
total_bytes = batch_size * seq_len * bytes_per_token
```

This is exactly why `[../01-attention-mechanisms/03-multi-query-attention]` and `[../01-attention-mechanisms/04-grouped-query-attention]` matter operationally: switching `kv_heads` from `n_heads` (MHA) down to a small `n_kv_heads` (GQA) or `1` (MQA) shrinks this formula linearly, directly translating into either a larger supportable batch size or a longer supportable context length for the same GPU memory budget.

### How PyTorch actually implements this

This is a pure scalar calculation — there's no tensor math to port; the same Python function works identically whether the surrounding model is implemented in NumPy or PyTorch. Real serving frameworks (vLLM's `gpu_memory_utilization` config, for example) compute exactly this formula to decide how many requests can fit in a given GPU's memory before even loading a single weight.

## Explanation

The mapping from attention variant to `kv_heads` is the only place the three variants differ; once `kv_heads` is fixed, the byte count is just the product of every dimension the cache spans (layers × heads × head-dim × elements × tokens × batch) times 2 for storing both K and V. Because the formula is linear in `kv_heads`, halving `kv_heads` (e.g. GQA with `n_kv_heads = n_heads / 2`) exactly halves the cache size — this direct proportionality is what makes "how many KV heads" a clean, predictable dial for trading model quality against serving capacity, unlike most other memory-saving techniques which have more complicated, non-linear trade-off curves.
