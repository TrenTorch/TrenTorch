---
name: research-fa2-num-blocks
title: 'FlashAttention-2: Partitioning Work Into Blocks'
tags: [research-papers, systems, attention, kernels]
difficulty: Beginner
---

## Statement

### The problem, from first principles

FlashAttention-2 assigns thread blocks to query blocks so that GPU streaming multiprocessors stay busy. The number of such blocks determines how many can run in parallel.

### From theory to code

Implement `num_blocks(n, block)`, the ceiling of n divided by the block size.

### Constraints

- Round up for a partial final block.

### Hints

<details>
<summary>Hint 1</summary>

Use integer ceiling division.

</details>

## Theory

### The simple version

If there are fewer query blocks than streaming multiprocessors, part of the GPU sits idle. Partitioning along the sequence keeps every processor busy, which the paper's second version improves.

### The formula

$$B = \left\lceil \frac{n}{b} \right\rceil$$

### How NumPy/PyTorch actually implements this

Kernel launch configuration in FlashAttention computes the grid size with the same ceiling division.

## Explanation

The rounding up accounts for the last, shorter tile that still needs a full kernel launch.
