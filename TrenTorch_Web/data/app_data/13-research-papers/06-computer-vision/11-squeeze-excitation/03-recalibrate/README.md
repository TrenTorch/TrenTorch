---
name: research-se-recalibrate
title: 'Squeeze-and-Excitation: Recalibrating the Features'
tags: [research-papers, computer-vision, attention, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

After the gates are computed, the block multiplies each channel of the original feature map by its gate. The gate is the same at every spatial position, so the whole channel is scaled.

### From theory to code

Implement `recalibrate(x, s)`, scaling each channel of the feature map by its gate.

### Constraints

- The gates broadcast over height and width.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the map by the gate vector, which NumPy broadcasts over the last axis.

</details>

## Theory

### The simple version

The block changes the relative strength of channels, letting the network emphasize informative features and suppress less useful ones, at very little cost.

### The formula

$$\tilde x_{i,j,c} = s_c\,x_{i,j,c}$$

### How NumPy/PyTorch actually implements this

SE blocks finish with `x * scale.view(b, c, 1, 1)`, which is the same channel-wise multiplication.

## Explanation

Because the scaling is per channel, it is an element-wise product with a vector broadcast over space.
