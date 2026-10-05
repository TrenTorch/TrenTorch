---
name: research-gqa-expand-kv
title: 'Grouped-Query Attention: Expanding Key-Value Heads'
tags: [research-papers, systems, attention, inference]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

In grouped-query attention, each key-value head serves a group of query heads. Before the attention product, the key and value heads are repeated so that every query head finds its group's copy.

### From theory to code

Implement `expand_kv(kv, n_heads)`, repeating each key-value head across its group.

### Constraints

- `n_heads` is a multiple of the number of key-value heads.

### Hints

<details>
<summary>Hint 1</summary>

Repeat along the head axis by the group size, keeping groups in order.

</details>

## Theory

### The simple version

The repeat is cheap for compute but must not change the cache: the stored tensor keeps one copy per group, and expansion happens on the fly.

### The formula

$$K_h = K_{\lfloor h/(H/G)\rfloor}$$

### How NumPy/PyTorch actually implements this

Inference kernels index the stored key-value heads with the group mapping instead of materializing the repeat.

## Explanation

`np.repeat` with `axis=0` produces the consecutive copies that match the group index mapping.
