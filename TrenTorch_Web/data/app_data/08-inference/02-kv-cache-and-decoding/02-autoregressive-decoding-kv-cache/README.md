---
name: inf-kv-autoregressive-cache
title: 'Autoregressive Generation with a KV Cache: prefill then decode'
tags: [inference, kv-cache, decoding, autoregressive]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Without caching, generating token `t+1` naively means re-running the whole sequence through the model again, recomputing keys and values for every position — `O(t)` wasted work per step. Since keys and values for already-seen positions never change (they only depend on the frozen input token at that position), they can be computed once and reused. Implement single-head causal self-attention generation with a KV cache: a "prefill" pass over the whole prompt at once (building the initial cache), then generating `n_new_tokens` one at a time, each time appending only the new token's key/value to the cache instead of recomputing the whole sequence.

### From theory to code

```
# Prefill: compute K, V once for every prompt position and cache them.
K_cache, V_cache = X_prompt @ W_K, X_prompt @ W_V

# Each decode step, compute K/V ONLY for the new token, append to cache.
k_new, v_new = x_new @ W_K, x_new @ W_V;  K_cache <- concat(K_cache, k_new)

# Attend the new token's query against the FULL cache (old + new).
out_new = softmax(q_new @ K_cache^T / sqrt(d_k)) @ V_cache
```

### Constraints

- Prefill must process the full prompt in a single batched causal attention call and populate the cache.
- Each decode step computes Q/K/V for exactly the single new token (not the whole running sequence).
- The new query attends over the entire cache including the just-appended new K/V (self-attention).
- Return the final generated hidden states for the new tokens AND the final cache length.

### Hints

<details>
<summary>Hint: Never recompute cached rows</summary>

Prefill is just standard causal attention over the whole prompt — reuse `[../01-attention-mechanisms/01-scaled-dot-product-attention]`'s masked-softmax machinery for it. In the decode loop, only ever concatenate ONE new row onto `K_cache`/`V_cache` per step — recomputing cached rows anywhere in the loop defeats the entire point of this exercise.

</details>

## Theory

### The simple version

Imagine writing a story one word at a time, where every earlier word's "meaning in context" (its key/value) never changes once it's written. Instead of re-reading and re-analyzing the whole story so far every time you add a word, you keep a running notebook of each word's meaning, and only add ONE new entry each time — never flipping back to rewrite earlier pages.

### The formula

```
K_cache, V_cache = X_prompt @ W_K, X_prompt @ W_V        # prefill, once
for each new token x_new:
    k_new, v_new = x_new @ W_K, x_new @ W_V
    K_cache = concat(K_cache, k_new);  V_cache = concat(V_cache, v_new)
    out_new = softmax(q_new @ K_cache^T / sqrt(d_k)) @ V_cache
```

The **prefill** phase processes the whole prompt in one batched forward pass (compute-bound, GPU-friendly). Each subsequent **decode** step then only computes Q/K/V for the single new token, turning per-step cost from `O(t)` new K/V projections down to `O(1)` — attention itself is still `O(t)` per step since the new query must scan `t` cached keys, but the expensive projection matmuls no longer get repeated.

### How PyTorch actually implements this

```python
def solve(X_prompt, W_Q, W_K, W_V, new_tokens):
    import torch
    d_k = W_K.shape[1]
    K_cache, V_cache = X_prompt @ W_K, X_prompt @ W_V
    Q_p = X_prompt @ W_Q
    prompt_len = X_prompt.shape[0]
    causal = torch.tril(torch.ones(prompt_len, prompt_len))
    scores = (Q_p @ K_cache.T / d_k**0.5).masked_fill(causal == 0, float("-inf"))
    prefill_out = torch.softmax(scores, dim=-1) @ V_cache
    outputs = []
    for x_new in new_tokens:
        q_new, k_new, v_new = x_new @ W_Q, x_new @ W_K, x_new @ W_V
        K_cache = torch.cat([K_cache, k_new[None]], dim=0)
        V_cache = torch.cat([V_cache, v_new[None]], dim=0)
        w = torch.softmax(K_cache @ q_new / d_k**0.5, dim=-1)
        outputs.append(w @ V_cache)
    return prefill_out, torch.stack(outputs), K_cache.shape[0]
```

Every real inference server (vLLM, TGI, TensorRT-LLM) implements exactly this prefill/decode split — `[03-kv-cache-memory-footprint]` quantifies the cost of the cache this builds up.

## Explanation

Because keys and values for a fixed input token never depend on any token that comes after it, appending exactly one new row to `K_cache`/`V_cache` per decode step and leaving earlier rows untouched produces exactly the same cache as recomputing K/V for the entire sequence-so-far at every step — the only thing saved is the redundant work. This is a purely algebraic optimization, not an approximation: a decode step's output is mathematically identical whether the cache was built incrementally or recomputed from scratch each time, since both compute the same `softmax(q_new @ K^T) @ V` over the identical set of keys and values.
