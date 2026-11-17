---
name: research-gqa-group-index
title: 'Grouped-Query Attention: Which Group Is a Head In?'
tags: [research-papers, systems, attention, inference]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Grouped-query attention (Ainslie et al., 2023) sits between multi-head and multi-query attention. Query heads are split into groups, and each group shares one key-value head. The grouping is a simple integer division.

### From theory to code

Implement `group_index(head, n_heads, n_kv)`, returning the key-value head used by a query head.

### Constraints

- Query heads are assigned to groups in contiguous blocks.

### Hints

<details>
<summary>Hint 1</summary>

Each group has `n_heads / n_kv` query heads, so divide the head index by that group size.

</details>

## Theory

### The simple version

The number of groups sets the cache size: one group is multi-query, and one group per head is standard multi-head. Grouped attention picks a point in between.

### The formula

$$g(h) = \left\lfloor \frac{h}{H/G}\right\rfloor$$

### How NumPy/PyTorch actually implements this

GQA implementations repeat each key-value head `H / G` times, indexed by this same group mapping.

## Explanation

Integer division by the group size gives a contiguous assignment, which is what the paper uses when converting checkpoints.
