---
name: research-scaled-dot-attention
title: 'Attention Is All You Need: Scaled Dot-Product Attention'
tags: [research-papers, transformers, llm, attention, transformer]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Attention Is All You Need (Vaswani et al., 2017) drops recurrence entirely. Each position builds its output by comparing a query with every key, turning the similarities into weights, and averaging the values with those weights. Dividing by the square root of the key dimension keeps the softmax from saturating.

### From theory to code

Implement `scaled_dot_product_attention(Q, K, V)`, which returns `softmax(Q K^T / sqrt(d)) V` with a row-wise softmax.

### Constraints

- `Q` and `K` share the feature dimension `d`.

### Hints

<details>
<summary>Hint 1</summary>

Compute `Q @ K.T / sqrt(d)`, apply a row-wise softmax with the max-subtraction trick, then multiply by `V`.

</details>

## Theory

### The simple version

Each query picks out the values whose keys match it best. The `sqrt(d)` scale matters: without it, dot products grow with dimension and push the softmax into a regime with almost no gradient.

### The formula

$$\operatorname{Attention}(Q, K, V) = \operatorname{softmax}\!\left(\frac{Q K^\top}{\sqrt{d_k}}\right) V$$

### How NumPy/PyTorch actually implements this

`torch.nn.functional.scaled_dot_product_attention` implements this formula, with fused kernels for speed.

## Explanation

The max subtraction is applied per row, so each query's weights are normalized independently.
