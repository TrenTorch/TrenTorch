---
name: research-lars-layer-norms
title: 'LARS: Per-layer Norms'
tags: [research-papers, optimization, large-batch]
difficulty: Beginner
---

## Statement

### The problem, from first principles

LARS needs a norm per layer, not one global norm. A weight tensor's norm is taken over all its entries, which is the Frobenius norm for a matrix.

### From theory to code

Implement `layer_norms(layers)`, returning each layer's weight norm.

### Constraints

- Layers are kept separate.

### Hints

<details>
<summary>Hint 1</summary>

Map the Euclidean norm over the list of layer arrays.

</details>

## Theory

### The simple version

A single global norm would let one large layer dominate the scaling of all the others, so norms are computed per layer.

### The formula

$$\lVert W\rVert_F = \sqrt{\sum_{ij}W_{ij}^2}$$

### How NumPy/PyTorch actually implements this

Frameworks compute the same per-tensor norms with `torch.norm` over each parameter.

## Explanation

The 2x2 ones matrix has Frobenius norm sqrt(4) = 2, which the last test checks.
