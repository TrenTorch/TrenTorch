---
name: research-mqa-kv-elems
title: 'Multi-Query Attention: KV Cache Elements'
tags: [research-papers, systems, attention, inference]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Multi-query attention (Shazeer, 2019) shares a single key and value head across all query heads. The query heads still differ, but the cache that decoding must read is much smaller, which speeds up incremental generation.

### From theory to code

Implement `kv_cache_elems(layers, kv_heads, seq, d_head)`, counting the cached key and value elements.

### Constraints

- For multi-query attention, `kv_heads` is 1.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the two (keys and values) by the layers, kv heads, sequence length and head dimension.

</details>

## Theory

### The simple version

Decoding is memory bound on reading the cache, so cutting the number of stored key-value heads speeds up each generated token.

### The formula

$$M_{\text{KV}} = 2\,L\,h_{kv}\,T\,d_{\text{head}}$$

### How NumPy/PyTorch actually implements this

Models such as PaLM use multi-query attention, and the cache size follows this formula.

## Explanation

Reducing `h_kv` from the number of query heads down to one is the saving the paper measures.
