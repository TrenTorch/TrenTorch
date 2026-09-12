---
name: inf-attn-multi-query
title: 'Multi-Query Attention: sharing one KV head across all query heads'
tags: [inference, attention, transformers, mqa, kv-cache]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[02-multi-head-attention]`'s per-token KV cache grows with `n_heads` — at long context lengths and large batch sizes this becomes the dominant memory cost during decoding, not the model weights. Multi-Query Attention (MQA) fixes this: every query head still has its own learned projection, but all query heads **share a single** key head and a single value head, shrinking the KV cache by a factor of `n_heads` with only a modest quality cost.

### From theory to code

Implement `multi_query_attention(X, W_Q, W_K, W_V, W_O, n_heads, mask=None)`:

```
Q_h = X @ W_Q[h] for h = 1..n_heads;   K = X @ W_K;   V = X @ W_V
head_h = softmax(Q_h K^T / sqrt(d_head)) @ V     -- every head uses the SAME K, V
output = concat(head_1, ..., head_H) @ W_O
```

### Constraints

- `Q` is split into `n_heads` heads of size `d_head = d_model // n_heads`, same as MHA.
- `K` and `V` are each a single `(seq_len, d_head)` matrix, shared across every query head — `W_K`, `W_V` project to `d_head`, not `d_model`.
- Attention scale and masking rules are identical to `[01-scaled-dot-product-attention]`.
- Output projection `W_O` has shape `(n_heads * d_head, d_model)`.

### Hints

<details>
<summary>Hint: No head loop needed for the shared K/V</summary>

`K` and `V` are 2D `(seq_len, d_head)` — do NOT reshape them per-head like in MHA. `Q @ K.T` naturally broadcasts the single key matrix against every one of the `n_heads` query slices when `Q` has shape `(n_heads, seq_len, d_head)`, so no explicit repeat or loop over heads is needed.

</details>

## Theory

### The simple version

Imagine `n_heads` analysts (queries), each with their own specialty and their own way of framing questions, but all of them consulting the exact same shared reference library (one K/V) instead of each analyst keeping a private copy of the entire library. The library takes far less space to store, and each analyst can still ask their own distinct questions of it.

### The formula

```
Q_h = X @ W_Q[h]  for h = 1..n_heads;   K = X @ W_K;   V = X @ W_V
head_h = softmax(Q_h K^T / sqrt(d_head)) @ V
output = concat(head_1, ..., head_H) @ W_O
```

During autoregressive decoding, memory bandwidth — not compute — is usually the bottleneck, and a smaller KV cache means fewer bytes to read per generated token. `[../02-kv-cache-and-decoding/03-kv-cache-memory-footprint]` quantifies exactly how much this saves.

### How PyTorch actually implements this

```python
def solve(X, W_Q, W_K, W_V, W_O, n_heads, mask=None):
    import torch, torch.nn.functional as F
    seq_len, d_model = X.shape
    d_head = W_K.shape[1]
    Q = (X @ W_Q).view(seq_len, n_heads, d_head).transpose(0, 1)
    K, V = X @ W_K, X @ W_V
    scores = Q @ K.T / d_head**0.5
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float("-inf"))
    heads = F.softmax(scores, dim=-1) @ V
    concat = heads.transpose(0, 1).reshape(seq_len, n_heads * d_head)
    return concat @ W_O
```

Models like PaLM and Falcon use MQA specifically for this inference-time memory saving.

## Explanation

Because `K` and `V` have no head axis, `Q @ K.T` naturally broadcasts the single `(seq_len, d_head)` key matrix against every one of the `n_heads` query slices — which is exactly the sharing MQA requires, with no explicit head loop or repeat needed. This is the same NumPy broadcasting rule that lets a `(seq_len, d_head)` array participate in a batched matmul against a `(n_heads, seq_len, d_head)` array without being reshaped first: broadcasting treats the missing leading axis as implicitly repeated across all `n_heads`, which is mathematically identical to physically repeating `K` and `V` `n_heads` times but without the extra memory allocation.
