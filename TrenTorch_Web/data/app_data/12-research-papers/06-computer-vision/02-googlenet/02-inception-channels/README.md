---
name: research-googlenet-inception-channels
title: 'GoogLeNet: Output Channels of an Inception Module'
tags: [research-papers, computer-vision, cnn, inception]
difficulty: Beginner
---

## Statement

### The problem, from first principles

An inception module runs four branches side by side and concatenates their outputs along the channel axis. Its output width is therefore the sum of the branch widths.

### From theory to code

Implement `inception_out_channels(c1, c3, c5, cp)`, the total output channels of one module.

### Constraints

- Returns an integer.

### Hints

<details>
<summary>Hint 1</summary>

Add the four branch widths.

</details>

## Theory

### The simple version

Concatenation lets each branch specialize in one scale, and the next layer sees all of them together. The channel sum is what the next module's input width must match.

### The formula

$$C_{\text{out}} = C_{1\times1} + C_{3\times3} + C_{5\times5} + C_{\text{pool}}$$

### How NumPy/PyTorch actually implements this

`torch.cat([b1, b3, b5, bp], dim=1)` concatenates the branches in the same way.

## Explanation

The branch outputs must share the spatial size, which the paper enforces with padding in each branch.
