---
name: research-chinchilla-flops
title: 'Chinchilla: Estimating Training FLOPs'
tags: [research-papers, transformers, llm, scaling, compute]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Hoffmann et al. (2022) ask how to split a fixed compute budget between model size and training data. The first ingredient is an estimate of how much compute a training run costs, which depends on the number of parameters and the number of tokens seen.

### From theory to code

Implement `training_flops(n_params, n_tokens)`, returning `6 * N * D`.

### Constraints

- `N` is parameters and `D` is training tokens.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the parameter count, the token count, and the constant 6.

</details>

## Theory

### The simple version

The factor 6 comes from the forward and backward passes: about 2 operations per parameter per token for the forward pass, and about 4 for the backward pass.

### The formula

$$C \approx 6\,N\,D$$

### How NumPy/PyTorch actually implements this

Training cost calculators use the same product, usually reported in petaFLOP-days.

## Explanation

This estimate is the standard rule of thumb used when planning large training runs, and it is what the Chinchilla analysis is built on.
