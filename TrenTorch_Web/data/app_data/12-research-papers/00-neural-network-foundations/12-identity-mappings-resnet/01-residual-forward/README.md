---
name: research-residual-forward
title: 'Identity Mappings in ResNet: The Residual Block'
tags: [research-papers, architecture, resnet]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Residual networks (He et al., 2016) add the block's input back to its output, so each block learns a residual on top of an identity path. The identity shortcut is what lets very deep networks train.

### From theory to code

Implement `residual_forward(x, f)`, which returns `x + f(x)`.

### Constraints

- `f` must return the same shape as `x`.

### Hints

<details>
<summary>Hint 1</summary>

Call `f` once and add the result to `x`.

</details>

## Theory

### The simple version

If `f` learns nothing, the block is the identity, so extra depth cannot make the function worse at initialization. The shortcut also gives gradients a direct path back.

### The formula

$$y = x + \mathcal{F}(x)$$

### How NumPy/PyTorch actually implements this

`torch` ResNet blocks compute `x + self.block(x)`, the same expression.

## Explanation

The addition is the only extra operation; there are no extra parameters for the shortcut.
