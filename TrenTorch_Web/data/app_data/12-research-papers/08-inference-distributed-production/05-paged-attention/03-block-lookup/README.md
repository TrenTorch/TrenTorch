---
name: research-vllm-block-lookup
title: 'PagedAttention: Finding a Token's Block'
tags: [research-papers, systems, serving, kv-cache]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

PagedAttention keeps a block table per sequence, mapping logical block numbers to physical memory blocks. Attention kernels use this table to find each cached token, so the blocks need not be contiguous in memory.

### From theory to code

Implement `block_table_lookup(block_table, token_idx, block_size)`, returning the physical block and offset of a token.

### Constraints

- Logical block is `token_idx // block_size`.

### Hints

<details>
<summary>Hint 1</summary>

Divide the token index by the block size to get the logical block, look it up in the table, and take the remainder as the offset.

</details>

## Theory

### The simple version

Indirection through the table is what lets blocks be scattered in GPU memory and shared between sequences, such as for prompt prefixes.

### The formula

$$b = \text{table}\big[\lfloor i/B\rfloor\big], \qquad o = i \bmod B$$

### How NumPy/PyTorch actually implements this

The vLLM attention kernel reads the table for each query to gather keys and values from scattered blocks.

## Explanation

The divide and remainder pair is the same address translation a virtual memory system performs.
