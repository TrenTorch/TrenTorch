---
name: research-vllm-num-blocks
title: 'PagedAttention: Blocks for a Sequence'
tags: [research-papers, systems, serving, kv-cache]
difficulty: Beginner
---

## Statement

### The problem, from first principles

vLLM (Kwon et al., 2023) stores the key-value cache in fixed-size blocks, like virtual memory pages, instead of one big contiguous buffer per request. A sequence claims as many blocks as its tokens need.

### From theory to code

Implement `vllm_num_blocks(seq_len, block_size)`, the number of blocks a sequence occupies.

### Constraints

- Round up so a partly filled block is still allocated.

### Hints

<details>
<summary>Hint 1</summary>

Use integer ceiling division by the block size.

</details>

## Theory

### The simple version

Allocating by block removes most of the fragmentation of contiguous caches, so the server can fit more concurrent requests in the same GPU memory.

### The formula

$$\text{blocks} = \left\lceil\frac{L}{B}\right\rceil$$

### How NumPy/PyTorch actually implements this

The vLLM block manager performs this allocation whenever a request's length crosses a block boundary.

## Explanation

Blocks are allocated on demand as a sequence grows, so memory tracks the actual token count.
