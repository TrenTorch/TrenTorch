---
name: research-unet-skip-concat
title: 'U-Net: Concatenating Skip Connections'
tags: [research-papers, computer-vision, segmentation, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The skip connection in U-Net concatenates the encoder's features with the upsampled decoder features. The decoder then has both coarse context and fine spatial detail for the next convolution.

### From theory to code

Implement `skip_concat(enc, dec)`, joining the two feature maps along the channel axis.

### Constraints

- Both maps have the same height and width.

### Hints

<details>
<summary>Hint 1</summary>

Concatenate along the last axis.

</details>

## Theory

### The simple version

Concatenation keeps the encoder's fine detail separate from the decoder's upsampled features, instead of averaging them away as addition would.

### The formula

$$y = [\,x_{\text{enc}} \,\|\, x_{\text{dec}}\,] \in \mathbb{R}^{H \times W \times (C_1 + C_2)}$$

### How NumPy/PyTorch actually implements this

U-Net decoders call `torch.cat([enc, dec], dim=1)` on the channel dimension.

## Explanation

The concatenation doubles the channel count at each decoder stage, which the following convolution reduces again.
