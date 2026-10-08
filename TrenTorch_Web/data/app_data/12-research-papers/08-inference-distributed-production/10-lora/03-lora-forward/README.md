---
name: research-lora-forward
title: 'LoRA: The Adapted Forward Pass'
tags: [research-papers, systems, fine-tuning, adapters]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The adapted layer computes the frozen output plus the scaled low-rank path. Because that path is linear, the adapter can be merged into the weight after training, leaving inference cost unchanged.

### From theory to code

Implement `lora_forward(x, W, A, B, scale)`, the frozen layer plus the scaled LoRA path.

### Constraints

- Matrix shapes follow the docstring.

### Hints

<details>
<summary>Hint 1</summary>

Compute `x W^T`, compute `x A^T` then `B^T` for the adapter, scale it, and add.

</details>

## Theory

### The simple version

Merging is possible because the sum of two linear maps is one linear map. After merging, serving uses a single matrix multiply, so LoRA adds no inference latency.

### The formula

$$y = xW^\top + \frac{\alpha}{r}\,x A^\top B^\top = x\,(W + \tfrac{\alpha}{r}BA)^\top$$

### How NumPy/PyTorch actually implements this

Adapter libraries offer a merge method that folds this update into the base weights for deployment.

## Explanation

The equivalence in the last test is the merge identity, which holds exactly for the linear layer.
