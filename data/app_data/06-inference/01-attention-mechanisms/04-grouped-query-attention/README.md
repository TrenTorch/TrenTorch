---
name: inf-attn-grouped-query
title: 'Grouped-Query Attention: the middle ground between MHA and MQA'
tags: [inference, attention, transformers, gqa, kv-cache]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[03-multi-query-attention]`'s single shared KV head can hurt quality on larger models, but `[02-multi-head-attention]`'s per-head KV cache is expensive. Grouped-Query Attention (GQA), used in Llama 2/3 and Mistral, is the middle ground: query heads are partitioned into `n_kv_heads` equal-sized groups, and every query head in a group attends to the SAME key/value head. `n_kv_heads == n_heads` recovers exactly MHA; `n_kv_heads == 1` recovers exactly MQA.

### From theory to code

Implement `grouped_query_attention(X, W_Q, W_K, W_V, W_O, n_heads, n_kv_heads, mask=None)`:

```
Q_h = X @ W_Q[h]                            for h = 1..n_heads
K_g = X @ W_K[g],  V_g = X @ W_V[g]          for g = 1..n_kv_heads
head_h = softmax(Q_h K_g^T / sqrt(d_head)) @ V_g   where g = h // (n_heads / n_kv_heads)
```

### Constraints

- `n_heads` must be divisible by `n_kv_heads`.
- Query head `h` attends to KV group `floor(h / (n_heads / n_kv_heads))` — consecutive query heads are grouped in blocks of size `n_heads // n_kv_heads`.
- Reduces to MQA behavior when `n_kv_heads == 1` and to MHA behavior when `n_kv_heads == n_heads`.
- Same scaling/masking rules as `[01-scaled-dot-product-attention]`.

### Hints

<details>
<summary>Hint: Repeat, don't loop</summary>

`np.repeat(K, group_size, axis=0)` on the KV-head axis turns `n_kv_heads` KV groups into `n_heads` rows where query head `h`'s row is exactly its assigned group `h // group_size` — so the rest of the computation is byte-for-byte identical to MHA's batched matmul, no per-head Python branching needed.

</details>

## Theory

### The simple version

Instead of every analyst having their own private reference library (MHA, expensive) or all analysts sharing one single library (MQA, cheap but less flexible), split the analysts into a few teams, and give each TEAM its own shared library. More teams means more distinct viewpoints (closer to MHA); fewer teams means less memory (closer to MQA) — GQA lets you pick exactly how many teams.

### The formula

```
Q_h = X @ W_Q[h]                     for h = 1..n_heads
K_g = X @ W_K[g],  V_g = X @ W_V[g]   for g = 1..n_kv_heads
head_h = softmax(Q_h K_g^T / sqrt(d_head)) @ V_g,  g = h // (n_heads / n_kv_heads)
```

With `n_kv_heads` groups, the KV cache shrinks by a factor of `n_heads / n_kv_heads` compared to MHA (see `[../02-kv-cache-and-decoding/03-kv-cache-memory-footprint]`), while retaining more representational diversity than MQA, since different groups of query heads can still specialize against different keys/values.

### How PyTorch actually implements this

```python
def solve(X, W_Q, W_K, W_V, W_O, n_heads, n_kv_heads, mask=None):
    import torch, torch.nn.functional as F
    seq_len, d_model = X.shape
    d_head = d_model // n_heads
    group_size = n_heads // n_kv_heads
    Q = (X @ W_Q).view(seq_len, n_heads, d_head).transpose(0, 1)
    K = (X @ W_K).view(seq_len, n_kv_heads, d_head).transpose(0, 1).repeat_interleave(group_size, dim=0)
    V = (X @ W_V).view(seq_len, n_kv_heads, d_head).transpose(0, 1).repeat_interleave(group_size, dim=0)
    scores = Q @ K.transpose(-2, -1) / d_head**0.5
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float("-inf"))
    heads = F.softmax(scores, dim=-1) @ V
    concat = heads.transpose(0, 1).reshape(seq_len, d_model)
    return concat @ W_O
```

## Explanation

`np.repeat(K, group_size, axis=0)` turns `n_kv_heads` KV groups into `n_heads` rows where query head `h`'s row is exactly its assigned group `h // group_size` — so the rest of the computation is byte-for-byte identical to MHA's batched matmul. This is what makes GQA a strict generalization rather than a separate algorithm: setting `group_size = 1` (i.e. `n_kv_heads = n_heads`) makes the repeat a no-op and reproduces MHA exactly, while setting `group_size = n_heads` (i.e. `n_kv_heads = 1`) repeats a single KV group across every head, reproducing MQA exactly — both earlier questions in this track are literal special cases of this one function.
