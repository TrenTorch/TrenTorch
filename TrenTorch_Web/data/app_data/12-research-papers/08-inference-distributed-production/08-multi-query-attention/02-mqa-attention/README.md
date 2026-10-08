---
name: research-mqa-attention
title: 'Multi-Query Attention: Shared Keys and Values'
tags: [research-papers, systems, attention, inference]
difficulty: Advanced
---

## Statement

### The problem, from first principles

In multi-query attention every query head attends to the same keys and values. Each head keeps its own queries, so the model still learns different attention patterns, but only one set of keys and values is stored and read.

### From theory to code

Implement `multi_query_attention(q, k, v)`, computing attention for all heads against the shared keys and values.

### Constraints

- `k` and `v` have no head axis.

### Hints

<details>
<summary>Hint 1</summary>

Broadcast the shared keys across heads by using matrix products with the head axis first, then softmax and weight the shared values.

</details>

## Theory

### The simple version

Sharing the key and value projections changes the cache, not the set of attention patterns each head can express through its own queries.

### The formula

$$\text{head}_h = \operatorname{softmax}\!\left(\frac{Q_h K^\top}{\sqrt{d}}\right)V$$

### How NumPy/PyTorch actually implements this

PaLM and Falcon run this shared-key attention during decoding with the same computation.

## Explanation

The product `q @ k.T` broadcasts over the head axis, so one `k` serves every head.
