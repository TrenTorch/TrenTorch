---
name: research-flash-hbm-bytes
title: 'FlashAttention: Memory Traffic of Naive Attention'
tags: [research-papers, systems, attention, kernels]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Standard attention writes the full n by n score matrix to GPU high-bandwidth memory and reads it back. For long sequences that traffic, not the arithmetic, is the bottleneck. FlashAttention avoids storing the matrix.

### From theory to code

Implement `naive_attention_hbm_bytes(n, bytes_per)`, the bytes needed to store the full score matrix.

### Constraints

- Default precision is two bytes (fp16).

### Hints

<details>
<summary>Hint 1</summary>

Count the n squared scores and multiply by the bytes per score.

</details>

## Theory

### The simple version

The score matrix grows with the square of the sequence length, so doubling the context quadruples its memory traffic. Tiling keeps only blocks on chip, which is the paper's core idea.

### The formula

$$\text{bytes} = n^2 \cdot b$$

### How NumPy/PyTorch actually implements this

Profiling tools show this memory bandwidth cost directly on attention kernels.

## Explanation

This is the traffic that FlashAttention reduces by computing scores blockwise in on-chip SRAM.
