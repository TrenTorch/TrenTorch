---
name: research-llama-rmsnorm
title: 'LLaMA: RMS Normalization'
tags: [research-papers, transformers, llm, normalization, llama]
difficulty: Beginner
---

## Statement

### The problem, from first principles

LLaMA (Touvron et al., 2023) replaces LayerNorm with RMSNorm, a simpler normalization that rescales by the root mean square without subtracting the mean. It is cheaper and performs about as well.

### From theory to code

Implement `rmsnorm(x, g, eps)`, dividing each row by its root mean square and multiplying by the gain `g`.

### Constraints

- No mean subtraction and no bias term.

### Hints

<details>
<summary>Hint 1</summary>

Compute the mean of squares over the last axis, take the square root with `eps`, divide, then multiply by `g`.

</details>

## Theory

### The simple version

Rescaling alone controls the magnitude of activations. Dropping the mean subtraction removes one reduction, which saves compute at no measurable cost in quality.

### The formula

$$\operatorname{RMSNorm}(x) = \frac{x}{\sqrt{\frac{1}{d}\sum_i x_i^2 + \epsilon}}\; g$$

### How NumPy/PyTorch actually implements this

`torch.nn.RMSNorm` in recent PyTorch versions implements this, and LLaMA-family code uses the same formula.

## Explanation

This is LayerNorm without the centering step and without a bias, applied per token.
