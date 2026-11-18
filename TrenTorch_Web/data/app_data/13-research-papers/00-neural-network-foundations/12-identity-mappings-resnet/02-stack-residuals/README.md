---
name: research-residual-stack
title: 'Identity Mappings in ResNet: Stacking Blocks'
tags: [research-papers, architecture, resnet]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A deep residual network is a stack of blocks. Each block adds its residual to the running signal, so the output is the input plus a sum of block contributions. Stacking is the step that produces the paper's deep models.

### From theory to code

Implement `stack_residuals(x, fs)`, which applies each residual block in order, adding each block's output to its input.

### Constraints

- An empty list returns `x` unchanged.

### Hints

<details>
<summary>Hint 1</summary>

Loop over the functions, replacing the running output with `out + f(out)` each time.

</details>

## Theory

### The simple version

The depth of the network is just the length of the list. Each block sees the output of the previous one, which is why composition order matters.

### The formula

$$x_{l+1} = x_l + \mathcal{F}_l(x_l), \qquad x_L = x_0 + \sum_{l=0}^{L-1}\mathcal{F}_l(x_l)$$

### How NumPy/PyTorch actually implements this

A `torch.nn.Sequential` of residual modules implements this loop, one module at a time.

## Explanation

The unrolled sum shows that every block's contribution is added to the same identity path, which is what keeps gradients flowing.
