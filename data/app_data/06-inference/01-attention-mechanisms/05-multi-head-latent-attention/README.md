---
name: inf-attn-multi-head-latent
title: 'Multi-Head Latent Attention: compressing KV into a shared low-rank latent'
tags: [inference, attention, transformers, mla, kv-cache, deepseek]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`[03-multi-query-attention]` and `[04-grouped-query-attention]` reduce the KV cache by sharing K/V ACROSS heads. Multi-Head Latent Attention (MLA, used in DeepSeek-V2/V3) takes a different route: compress K and V for ALL heads into one small shared latent vector `c` of dimension `d_latent` (far smaller than `n_heads * d_head`), and reconstruct per-head keys/values from that latent on the fly. Implement a simplified version of this scheme.

### From theory to code

Implement `multi_head_latent_attention(X, W_Q, W_DKV, W_UK, W_UV, W_O, n_heads, mask=None)`:

```
c = X @ W_DKV                          # (seq_len, d_latent) -- this is what actually gets cached
K = c @ W_UK,   V = c @ W_UV            # up-project the latent into full per-head K, V
Q_h = X @ W_Q[h]                        # queries are computed directly, no compression
head_h = softmax(Q_h K_h^T / sqrt(d_head)) @ V_h;  output = concat(heads) @ W_O
```

### Constraints

- Compute latent `c = X @ W_DKV` once (shape `(seq_len, d_latent)`).
- Reconstruct full `K`, `V` via `K = c @ W_UK`, `V = c @ W_UV`, then reshape into `n_heads` heads.
- Queries are computed directly from `X` per head (no compression on the query side).
- Return both the attention output and the latent cache `c` — what would actually be stored per token in a real KV cache.
- `d_latent < n_heads * d_head` (a real compression, not a no-op).

### Hints

<details>
<summary>Hint: Reuse the MHA attention loop</summary>

First compute the latent `c = X @ W_DKV` once per token — this is the only thing you'd persist in a real KV cache. Up-project `c` into `K` and `V` using `W_UK`/`W_UV`, reshape into per-head form exactly like `[02-multi-head-attention]`, then reuse that same attention computation unchanged.

</details>

## Theory

### The simple version

Instead of every head keeping its own full notebook of keys and values (MHA), or all heads sharing one notebook (MQA), imagine compressing everything worth remembering into one tiny index card per token (the latent `c`), then, whenever a head actually needs to look something up, expanding that index card back out into the specific details it needs. Storing the index cards takes far less space than storing full notebooks.

### The formula

```
c = X @ W_DKV                           # (seq_len, d_latent), the cacheable artifact
K_full = c @ W_UK,   V_full = c @ W_UV  # (seq_len, n_heads * d_head)
Q_h = X @ W_Q[h]
head_h = softmax(Q_h K_h^T / sqrt(d_head)) @ V_h
output = concat(heads) @ W_O
```

Because `W_UK`/`W_UV` are fixed, learned matrices, this is mathematically a low-rank factorization of what would otherwise be a full-rank per-head K/V: `K_full = (X @ W_DKV) @ W_UK = X @ (W_DKV @ W_UK)`, a single projection whose rank is capped at `d_latent`.

### How PyTorch actually implements this

```python
def solve(X, W_Q, W_DKV, W_UK, W_UV, W_O, n_heads, mask=None):
    import torch, torch.nn.functional as F
    seq_len, d_model = X.shape
    d_head = d_model // n_heads
    c = X @ W_DKV
    K = (c @ W_UK).view(seq_len, n_heads, d_head).transpose(0, 1)
    V = (c @ W_UV).view(seq_len, n_heads, d_head).transpose(0, 1)
    Q = (X @ W_Q).view(seq_len, n_heads, d_head).transpose(0, 1)
    scores = Q @ K.transpose(-2, -1) / d_head**0.5
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float("-inf"))
    heads = F.softmax(scores, dim=-1) @ V
    concat = heads.transpose(0, 1).reshape(seq_len, d_model)
    return concat @ W_O, c
```

This is what lets DeepSeek-style models keep long-context KV caches dramatically smaller than an equivalent MHA/GQA model at the same quality.

## Explanation

Since `K_full = (X @ W_DKV) @ W_UK = X @ (W_DKV @ W_UK)`, the compression is mathematically equivalent to a single low-rank K projection `W_DKV @ W_UK` whose rank is capped at `d_latent` — the model can only express as many independent K directions as the latent has dimensions, which is exactly the storage saving: only `c` (width `d_latent`) needs to be cached, not the full-width K/V. This is a genuinely different lever than MQA/GQA's "share across heads": MLA compresses the INFORMATION CONTENT itself into a narrow bottleneck, so every head still gets its own reconstructed K/V (unlike MQA/GQA, where heads literally share the same values) — the saving comes from the latent's rank, not from head-sharing.
