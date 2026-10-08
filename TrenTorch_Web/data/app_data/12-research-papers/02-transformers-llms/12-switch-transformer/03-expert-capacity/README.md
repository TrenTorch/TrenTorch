---
name: research-switch-capacity
title: 'Switch Transformers: Expert Capacity'
tags: [research-papers, transformers, llm, moe, routing]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Experts run as fixed-size matrix multiplies, so each one can only take a set number of tokens per batch. Switch Transformers set that capacity from the average load times a slack factor, and tokens beyond it are dropped.

### From theory to code

Implement `expert_capacity(n_tokens, n_experts, capacity_factor)`, returning the integer capacity per expert.

### Constraints

- Round up to a whole number of tokens.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the factor by the average load per expert, then take the ceiling.

</details>

## Theory

### The simple version

Without slack, any imbalance drops tokens. A factor above 1 gives each expert headroom, trading a little extra compute for fewer dropped tokens.

### The formula

$$\text{capacity} = \left\lceil \frac{C\,T}{E} \right\rceil$$

### How NumPy/PyTorch actually implements this

MoE layers in training frameworks compute this same value to size each expert's buffer before dispatching tokens.

## Explanation

`C` is the capacity factor, `T` the number of tokens and `E` the number of experts; the ceiling makes it an integer buffer size.
