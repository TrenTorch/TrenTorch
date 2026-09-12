---
name: inf-attn-multi-head
title: 'Multi-Head Attention: splitting into independent heads'
tags: [inference, attention, transformers, multi-head]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[01-scaled-dot-product-attention]` computes one single attention pattern per call. But a single pattern can only capture one type of relationship per layer (e.g. "attend to the previous token"). Multi-Head Attention (MHA) splits a model-dimension input into `n_heads` independent attention heads, runs scaled dot-product attention in each head in parallel, then concatenates the head outputs and projects them back to the model dimension — so each head can learn a different attention pattern cheaply.

### From theory to code

Implement `multi_head_attention(X, W_Q, W_K, W_V, W_O, n_heads, mask=None)`:

```
Q_h = X @ W_Q[h],  K_h = X @ W_K[h],  V_h = X @ W_V[h]     for h = 1..n_heads
head_h = softmax(Q_h K_h^T / sqrt(d_head)) @ V_h
output = concat(head_1, ..., head_H) @ W_O
```

### Constraints

- `d_model` must be evenly divisible by `n_heads`; `d_head = d_model // n_heads`.
- Each head gets its own Q/K/V weight slice, all packed into single `(d_model, d_model)` matrices `W_Q`, `W_K`, `W_V`.
- Apply scaled dot-product attention (scale by `sqrt(d_head)`) independently per head.
- Concatenate heads in head order, then apply the output projection `W_O` of shape `(d_model, d_model)`.

### Hints

<details>
<summary>Hint 1: Splitting into heads without a loop</summary>

Reshape `(seq_len, d_model)` into `(seq_len, n_heads, d_head)` by splitting the last axis, then transpose to `(n_heads, seq_len, d_head)`. This is exactly equivalent to slicing `n_heads` separate weight matrices out of one big projection, and lets you do the whole thing as one batched matmul instead of a Python loop over heads.

</details>

<details>
<summary>Hint 2: Reassembling after attention</summary>

After computing `(n_heads, seq_len, d_head)` head outputs, transpose back to `(seq_len, n_heads, d_head)` and reshape to `(seq_len, d_model)` before the final `W_O` projection — this must invert exactly the split you did going in, in head order.

</details>

## Theory

### The simple version

A single reviewer reading a document can only focus on one thing at a time (e.g. "who's the subject of this sentence"). Multi-head attention is like handing the same document to several reviewers simultaneously, each told to look for something different (syntax, coreference, positional offset), then combining all their notes into one final summary.

### The formula

```
Q_h = X @ W_Q[h],  K_h = X @ W_K[h],  V_h = X @ W_V[h]   for h = 1..n_heads
head_h = softmax(Q_h K_h^T / sqrt(d_head)) @ V_h
output = concat(head_1, ..., head_H) @ W_O
```

At inference time, MHA is also the most memory-hungry attention variant: every head keeps its own full-size K/V cache. This is exactly the problem Multi-Query and Grouped-Query Attention (later questions in this track) exist to solve.

### How PyTorch actually implements this

```python
import torch, torch.nn.functional as F

def solve(X, W_Q, W_K, W_V, W_O, n_heads, mask=None):
    seq_len, d_model = X.shape
    d_head = d_model // n_heads
    Q, K, V = (t.view(seq_len, n_heads, d_head).transpose(0, 1) for t in (X @ W_Q, X @ W_K, X @ W_V))
    scores = Q @ K.transpose(-2, -1) / d_head**0.5
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float("-inf"))
    heads = F.softmax(scores, dim=-1) @ V
    concat = heads.transpose(0, 1).reshape(seq_len, d_model)
    return concat @ W_O
```

`torch.nn.MultiheadAttention` implements exactly this, with the `W_Q`/`W_K`/`W_V` packed into one `in_proj_weight` matrix internally.

## Explanation

Reshaping the last axis of a `(seq_len, d_model)` matrix into `(seq_len, n_heads, d_head)` and transposing to `(n_heads, seq_len, d_head)` is exactly equivalent to slicing `n_heads` separate weight matrices out of a single big projection — it's the standard trick that lets frameworks implement MHA as one batched matmul instead of a Python loop over heads. Because the split-then-transpose and transpose-then-merge steps are exact inverses of each other, doing the whole computation in `n_heads` batched calls produces byte-identical results to running `n_heads` separate single-head attention calls and concatenating them by hand — the batching is purely a performance optimization, never an approximation.
