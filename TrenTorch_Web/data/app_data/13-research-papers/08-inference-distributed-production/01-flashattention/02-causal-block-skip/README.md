---
name: research-flash-causal-block-skip
title: 'FlashAttention: Skipping Masked Blocks'
tags: [research-papers, systems, attention, kernels]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Causal attention masks out every future position, so many key blocks are completely masked for a given query block. FlashAttention skips those blocks entirely, saving about half the compute in a causal model.

### From theory to code

Implement `causal_block_needed(qb, kb, bq, bk)`, deciding whether a key block must be computed.

### Constraints

- Return a bool.

### Hints

<details>
<summary>Hint 1</summary>

A key block is needed if its first key index is at most the last query index in the query block.

</details>

## Theory

### The simple version

Skipping masked tiles is what turns the causal mask into real savings rather than wasted multiplications.

### The formula

$$\text{needed} \iff k_{\min} \le q_{\max}, \qquad k_{\min} = k_b\,B_k,\; q_{\max} = q_b\,B_q + B_q - 1$$

### How NumPy/PyTorch actually implements this

The FlashAttention kernels compute the same bound from block indices when they launch tiles.

## Explanation

The comparison is between two integers, so the test is free compared with the matrix product it avoids.
