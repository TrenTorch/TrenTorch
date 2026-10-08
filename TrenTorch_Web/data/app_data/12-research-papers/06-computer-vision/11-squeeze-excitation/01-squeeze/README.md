---
name: research-se-squeeze
title: 'Squeeze-and-Excitation: The Squeeze Step'
tags: [research-papers, computer-vision, attention, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Squeeze-and-Excitation (Hu et al., 2018) first summarizes each channel with a single number, its global average. That summary is what the network uses to decide how much to emphasize each channel.

### From theory to code

Implement `squeeze(x)`, the global average pooling over height and width.

### Constraints

- Returns one value per channel.

### Hints

<details>
<summary>Hint 1</summary>

Average over the first two axes.

</details>

## Theory

### The simple version

Channel-wise statistics are cheap to compute and give the network a global view of each feature map, which the excitation step then uses.

### The formula

$$z_c = \frac{1}{HW}\sum_{i=1}^{H}\sum_{j=1}^{W} x_{i,j,c}$$

### How NumPy/PyTorch actually implements this

The SE block calls `F.adaptive_avg_pool2d(x, 1)` on the feature map.

## Explanation

This is the global average pooling layer used at the end of many CNNs, applied here inside each block.
