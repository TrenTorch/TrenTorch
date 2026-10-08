---
name: research-dropout-backward
title: 'Dropout: Backpropagating Through the Mask'
tags: [research-papers, regularization, dropout]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Dropout zeroes random units during training, so the backward pass must treat those units the same way: a unit that was dropped in the forward pass contributed nothing to the output, so it receives no gradient.

### From theory to code

Implement `dropout_backward(grad_out, keep_mask, p)`, which multiplies the incoming gradient by the same mask and rescale used in the forward pass.

### Constraints

- `keep_mask` has the same shape as `grad_out`.
- `0 <= p < 1`.

### Hints

<details>
<summary>Hint 1</summary>

Use the exact mask and scale from the forward pass. Dropped units get a gradient of zero; kept units get the same `1 / (1 - p)` factor.

</details>

## Theory

### The simple version

The gradient flows back only through the units that were kept. The forward pass multiplied each kept unit by `1 / (1 - p)`, so the backward pass multiplies by the same factor.

### The formula

$$\frac{\partial L}{\partial h} = \frac{m \odot \partial L / \partial \tilde h}{1 - p}$$

### How NumPy/PyTorch actually implements this

`torch.nn.functional.dropout` records its mask and autograd applies the same gating and scale automatically during backpropagation.

## Explanation

`dropout_backward` multiplies the incoming gradient by `keep_mask` and by `1 / (1 - p)`, mirroring the forward pass. Using the same mask is what makes the gradient correct for that specific random sample.
