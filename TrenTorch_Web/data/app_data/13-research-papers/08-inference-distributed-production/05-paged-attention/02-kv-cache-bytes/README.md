---
name: research-vllm-kv-cache-bytes
title: 'PagedAttention: KV Cache Size'
tags: [research-papers, systems, serving, kv-cache]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

During generation a transformer keeps keys and values for every past token, in every layer. This KV cache is often the largest memory consumer at inference, and it sets how many requests a GPU can serve at once.

### From theory to code

Implement `kv_cache_bytes(layers, heads, d, seq, nbytes)`, the cache size for one sequence.

### Constraints

- Keys and values are both stored.

### Hints

<details>
<summary>Hint 1</summary>

Multiply two (keys and values) by the layers, heads, head dimension, sequence length and bytes per element.

</details>

## Theory

### The simple version

The cache grows with every token generated, so long contexts and large batches compete for the same memory. Paging makes that competition efficient.

### The formula

$$M_{\text{KV}} = 2\cdot L\cdot h\cdot d\cdot T\cdot b$$

### How NumPy/PyTorch actually implements this

Serving dashboards estimate capacity from this formula before choosing a batch size.

## Explanation

The factor two is keys and values; the cache holds one entry per token per layer per head.
