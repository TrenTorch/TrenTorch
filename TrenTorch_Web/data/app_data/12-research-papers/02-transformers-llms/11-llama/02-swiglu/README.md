---
name: research-llama-swiglu
title: 'LLaMA: The SwiGLU Feed-Forward Gate'
tags: [research-papers, transformers, llm, feedforward, llama]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The feed-forward layer in LLaMA multiplies two projections of the input, one of them passed through a SiLU (Swish) nonlinearity. This gated linear unit, called SwiGLU, performs better than the plain ReLU MLP at similar size.

### From theory to code

Implement `swiglu(x, W, V)`, returning `silu(x W) * (x V)`.

### Constraints

- `silu(z) = z * sigmoid(z)`.

### Hints

<details>
<summary>Hint 1</summary>

Project with `W`, apply `silu`, project with `V`, and multiply element-wise.

</details>

## Theory

### The simple version

The gate decides which hidden features pass through. Because the gate is smooth and the up projection is linear, the network has a richer way to combine features than a single nonlinearity.

### The formula

$$\operatorname{SwiGLU}(x) = \operatorname{SiLU}(xW) \odot (xV), \qquad \operatorname{SiLU}(z) = z\,\sigma(z)$$

### How NumPy/PyTorch actually implements this

`torch.nn.functional.silu(x @ W) * (x @ V)` is the standard implementation in LLaMA-family models.

## Explanation

The SiLU is the same function as Swish with beta 1. The element-wise product is the gating.
