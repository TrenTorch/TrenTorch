---
name: research-llama-hidden-dim
title: 'LLaMA: Choosing the Feed-Forward Width'
tags: [research-papers, transformers, llm, feedforward, llama]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

SwiGLU has three weight matrices instead of two, so to keep the parameter count matched to a standard feed-forward layer, the hidden width is set to about two thirds of four times the model width. The result is rounded up to a hardware-friendly multiple.

### From theory to code

Implement `llama_hidden_dim(dim, multiple_of)`, returning `int(8 * dim / 3)` rounded up to a multiple of `multiple_of`.

### Constraints

- The default multiple is 256.

### Hints

<details>
<summary>Hint 1</summary>

Compute `int(2 * 4 * dim / 3)`, then round up with integer arithmetic.

</details>

## Theory

### The simple version

Rounding up to a multiple of 256 keeps matrix shapes aligned for efficient hardware kernels, at a tiny cost in parameters.

### The formula

$$h = \left\lceil \frac{8d}{3} \right\rceil_{\text{multiple}}$$

### How NumPy/PyTorch actually implements this

Model configs in LLaMA-family code set this width explicitly; the formula reproduces those values.

## Explanation

The `8/3` factor is the reason the SwiGLU block has the same parameter count as a `4d` ReLU block: three matrices of width `8d/3` cost the same as two of width `4d`.
