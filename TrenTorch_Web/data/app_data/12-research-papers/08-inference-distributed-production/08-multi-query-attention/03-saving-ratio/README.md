---
name: research-mqa-saving-ratio
title: 'Multi-Query Attention: The Cache Saving Ratio'
tags: [research-papers, systems, attention, inference]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The benefit of multi-query attention is a ratio: each key-value head removed from the cache saves its share of memory and bandwidth. The ratio of query heads to key-value heads is that saving.

### From theory to code

Implement `saving_ratio(H, kv_heads)`, the cache reduction factor.

### Constraints

- Returns a float.

### Hints

<details>
<summary>Hint 1</summary>

Divide the query head count by the key-value head count.

</details>

## Theory

### The simple version

Decoding time roughly tracks cache bytes read per token, so the same ratio predicts the speed-up for memory-bound decoding.

### The formula

$$\rho = \frac{H}{h_{kv}}$$

### How NumPy/PyTorch actually implements this

Architecture comparisons in model cards list the query and key-value head counts from which this ratio follows.

## Explanation

The ratio is exact for the cache size; the realized speed-up is smaller because other computation remains.
