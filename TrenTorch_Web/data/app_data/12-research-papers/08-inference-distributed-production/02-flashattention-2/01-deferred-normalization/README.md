---
name: research-fa2-deferred-normalization
title: 'FlashAttention-2: Deferred Normalization'
tags: [research-papers, systems, attention, kernels]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

FlashAttention-2 (Dao, 2023) reduces non-matmul work by keeping the output unnormalized while streaming over key blocks, and dividing by the softmax denominator only once at the end.

### From theory to code

Implement `finalize_output(acc, l)`, dividing the accumulator by the denominator row by row.

### Constraints

- `l` has one entry per query row.

### Hints

<details>
<summary>Hint 1</summary>

Divide each row of the accumulator by its denominator, broadcasting over the feature axis.

</details>

## Theory

### The simple version

A single division per row, instead of a rescale every block, cuts the scalar work that GPUs execute slowly compared with matrix multiplies.

### The formula

$$O = \frac{\tilde O}{\ell}$$

### How NumPy/PyTorch actually implements this

FlashAttention-2 kernels perform this final normalization in registers before writing the output.

## Explanation

Deferring the division is exact because the denominator is a per-row scalar that commutes with the weighted sum.
