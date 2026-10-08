---
name: research-gqa-groups-valid
title: 'Grouped-Query Attention: Valid Group Counts'
tags: [research-papers, systems, attention, inference]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Grouped-query attention only works when the query heads divide evenly into groups. Checking that before building a model prevents a silent mismatch between head counts and cache shapes.

### From theory to code

Implement `groups_valid(n_heads, n_kv)`, returning whether the grouping is well defined.

### Constraints

- Returns a bool.

### Hints

<details>
<summary>Hint 1</summary>

Check the group count is between one and the head count and divides it exactly.

</details>

## Theory

### The simple version

A bad head configuration would produce wrong group indices or a shape error deep in the model. Validating the config early gives a clear message.

### The formula

$$1 \le G \le H \;\land\; H \bmod G = 0$$

### How NumPy/PyTorch actually implements this

Model config classes check the same condition when a transformer config is created.

## Explanation

The divisibility condition is what makes the group size an integer.
