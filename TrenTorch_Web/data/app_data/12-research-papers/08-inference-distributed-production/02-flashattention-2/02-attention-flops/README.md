---
name: research-fa2-attention-flops
title: 'FlashAttention-2: Attention FLOPs'
tags: [research-papers, systems, attention, kernels]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Attention does two matrix multiplications per head, each costing about two n squared d operations. Knowing that count tells you whether a kernel is limited by compute or by memory.

### From theory to code

Implement `attention_flops(n, d, causal)`, the floating-point operations of one attention head.

### Constraints

- Causal attention does about half the work.

### Hints

<details>
<summary>Hint 1</summary>

Count four n squared d operations for the two products, then halve for causal masking.

</details>

## Theory

### The simple version

Comparing measured throughput with this count gives the hardware utilization the paper reports.

### The formula

$$\text{FLOPs} \approx 4\,n^2 d \quad(\text{causal: } 2\,n^2 d)$$

### How NumPy/PyTorch actually implements this

Benchmarking scripts divide measured time into this FLOP count to report achieved TFLOPs.

## Explanation

The factor four is two products times two operations per multiply-accumulate.
