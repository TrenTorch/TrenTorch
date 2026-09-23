---
name: seq-attention-grouped-query-attention
title: 'Stretch: Grouped-Query Attention (GQA)'
tags: [transformers]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`[04-mha-split-heads]`'s Multi-Head Attention gives every query head its OWN dedicated key and value head. During autoregressive text generation, a real serving system has to cache every previously-generated token's key and value vectors, for EVERY head (the "KV cache"), so they don't need to be recomputed at every single new generation step. With `num_heads` full-sized key/value heads, this cache grows LINEARLY with the number of heads, and for large modern models with many heads and long contexts, the KV cache can become the dominant memory cost of actually serving the model, often larger than the model's own weights for long enough sequences.

Grouped-Query Attention (Ainslie et al., 2023, used in Llama 2/3 and many other modern models) reduces this cost directly: keep the FULL number of query heads (queries are never cached across generation steps, so they don't contribute to this cost at all), but use FEWER key/value heads, with several query heads SHARING the same key/value head. This shrinks the KV cache by exactly the ratio `num_query_heads / num_kv_heads`, while empirically losing only a small amount of model quality compared to full Multi-Head Attention, a favorable, now widely-adopted tradeoff. (The extreme case, `num_kv_heads = 1`, a SINGLE shared key/value head for every query head, is called Multi-Query Attention, an even more aggressive predecessor to GQA.)

### From theory to code

Implement `repeat_kv_heads(x, num_repeats)`, repeating each key/value head CONSECUTIVELY `num_repeats` times along the head axis, so `(batch, num_kv_heads, seq_len, d_k)` becomes `(batch, num_kv_heads * num_repeats, seq_len, d_k)`. Implement `grouped_query_attention(query, key, value, num_query_heads, num_kv_heads, mask)`: split `query` into `num_query_heads` heads and `key`/`value` into `num_kv_heads` heads (both via `[04-mha-split-heads]`'s `split_heads`, already provided), repeat the key/value heads via `repeat_kv_heads` so their count matches `num_query_heads`, then call `[01-scaled-dot-product-attention]`'s `scaled_dot_product_attention` once on the now-matching-head-count inputs.

### Constraints

- `num_query_heads` must be evenly divisible by `num_kv_heads` (assume this holds).
- `repeat_kv_heads` must repeat each kv head CONSECUTIVELY (kv head 0 repeated `num_repeats` times in a row, THEN kv head 1 repeated `num_repeats` times, and so on), not interleaved.
- Query head `i` must end up paired with kv head `i // num_repeats` (where `num_repeats = num_query_heads // num_kv_heads`), the standard "contiguous group" convention.
- When `num_kv_heads == num_query_heads`, `grouped_query_attention` must reduce EXACTLY to ordinary Multi-Head Attention (`repeat_kv_heads` with `num_repeats=1` is the identity operation).

### Hints

<details>
<summary>Hint 1: repeat_kv_heads</summary>

`np.repeat(x, num_repeats, axis=1)` does exactly the "each element repeated consecutively `num_repeats` times" operation directly: `np.repeat([A, B], 2)` gives `[A, A, B, B]`, not `[A, B, A, B]` (that interleaved pattern would be `np.tile`, a genuinely different operation).

</details>

<details>
<summary>Hint 2: The overall pipeline</summary>

`query_heads = split_heads(query, num_query_heads)`, `key_heads = split_heads(key, num_kv_heads)`, `value_heads = split_heads(value, num_kv_heads)`. Compute `num_repeats = num_query_heads // num_kv_heads`, then `key_heads_repeated = repeat_kv_heads(key_heads, num_repeats)` and the same for `value_heads`.

</details>

<details>
<summary>Hint 3: Final call</summary>

`return scaled_dot_product_attention(query_heads, key_heads_repeated, value_heads_repeated, mask=mask)`: now that `key_heads_repeated`/`value_heads_repeated` have exactly `num_query_heads` heads too, matching `query_heads`, the existing attention function needs no changes at all to handle this.

</details>

## Theory

### The simple version

A restaurant kitchen where several individual chefs (query heads) each work on their OWN dish, but instead of each chef having a PERSONAL, dedicated spice rack (a full-sized key/value head each, expensive to stock and maintain many of), several chefs SHARE one spice rack between them, a smaller group of shared racks rather than one per chef. Each chef still cooks their own distinct dish (queries stay fully separate, never shared), but the shared, expensive-to-maintain resource (the spice rack, standing in for the KV cache) is provisioned more economically, with only a modest impact on any individual dish's quality.

### The formula

```
num_repeats = num_query_heads // num_kv_heads

query_heads = split_heads(query, num_query_heads)
key_heads   = repeat_kv_heads(split_heads(key,   num_kv_heads), num_repeats)
value_heads = repeat_kv_heads(split_heads(value, num_kv_heads), num_repeats)

output, weights = scaled_dot_product_attention(query_heads, key_heads, value_heads, mask)
```

Query head `i` (for `i = 0, ..., num_query_heads-1`) ends up paired against kv head `i // num_repeats`: heads `0` through `num_repeats-1` share kv head `0`, heads `num_repeats` through `2*num_repeats-1` share kv head `1`, and so on.

### How PyTorch actually implements this

Nothing in core `torch.nn` implements GQA directly (like RoPE, it's specific enough to modern LLM architectures that it lives in model-specific code, Hugging Face `transformers`' Llama implementation, for instance), but every real implementation performs exactly this "repeat the smaller set of kv heads to match the query head count" operation, often via `torch.repeat_interleave` (equivalent to this question's `np.repeat` with `axis` specified) rather than a full physical memory copy, some implementations instead reshape query heads into GROUPS and broadcast the kv heads across each group without ever materializing the repeated tensor at all, a memory-saving optimization that computes the SAME mathematical result as this question's more explicit, easier-to-follow version. `Note: FlashAttention`, later in this curriculum, and GQA are complementary, not competing, optimizations, FlashAttention reduces the memory and compute cost of the attention COMPUTATION itself, while GQA reduces the memory cost of the KV CACHE between generation steps, and modern production LLM serving systems typically use both simultaneously.

## Explanation

`repeat_kv_heads` calls `np.repeat(x, num_repeats, axis=1)`, NumPy's built-in "repeat each element consecutively" operation applied specifically to the head axis, turning `num_kv_heads` heads into `num_kv_heads * num_repeats` heads, with each original head appearing `num_repeats` times in a row.

`grouped_query_attention` splits `query` into its full `num_query_heads` heads, splits `key`/`value` into their smaller `num_kv_heads` heads, computes `num_repeats = num_query_heads // num_kv_heads`, and calls `repeat_kv_heads` on both the split key and value heads to expand them up to `num_query_heads` heads each, with the correct contiguous-group correspondence. With head counts now matching across all three inputs, it calls `scaled_dot_product_attention` exactly once, unchanged, letting it handle the (now equally-sized) leading head dimension the same way it always does.
