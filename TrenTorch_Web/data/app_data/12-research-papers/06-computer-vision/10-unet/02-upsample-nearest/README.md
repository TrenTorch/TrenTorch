---
name: research-unet-upsample
title: 'U-Net: Nearest-neighbour Upsampling'
tags: [research-papers, computer-vision, segmentation, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The U-Net decoder increases resolution step by step. A simple upsampling that copies each value into a block is cheap and avoids checkerboard artifacts from transposed convolutions.

### From theory to code

Implement `upsample_nearest(x, f)`, repeating each value into an f-by-f block.

### Constraints

- Works on maps with extra channel axes.

### Hints

<details>
<summary>Hint 1</summary>

Repeat along the height axis, then along the width axis.

</details>

## Theory

### The simple version

Nearest-neighbour upsampling keeps the average intensity and creates no new values, so the decoder learns the detail from the skip connections.

### The formula

$$y_{i,j} = x_{\lfloor i/f\rfloor,\;\lfloor j/f\rfloor}$$

### How NumPy/PyTorch actually implements this

`F.interpolate(x, scale_factor=f, mode='nearest')` performs this operation.

## Explanation

The mapping from output to input position is a floor division, which is the definition of nearest-neighbour sampling at integer factors.
