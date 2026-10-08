---
name: research-unet-crop
title: 'U-Net: Center-cropping Skip Connections'
tags: [research-papers, computer-vision, segmentation, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

U-Net (Ronneberger et al., 2015) copies high-resolution encoder features to the decoder through skip connections. Unpadded convolutions shrink the maps, so the copied features are center-cropped to match.

### From theory to code

Implement `center_crop(x, h, w)`, returning the central region of a feature map.

### Constraints

- The crop is centered; with an odd difference the extra row or column goes to the bottom or right.

### Hints

<details>
<summary>Hint 1</summary>

Compute the top and left offsets from the size difference, then slice.

</details>

## Theory

### The simple version

Cropping the encoder map to the decoder's size lets the two be concatenated. Centering keeps the features aligned with the decoder's output.

### The formula

$$\text{top} = \left\lfloor\frac{H - h}{2}\right\rfloor,\qquad \text{left} = \left\lfloor\frac{W - w}{2}\right\rfloor$$

### How NumPy/PyTorch actually implements this

U-Net implementations crop the encoder tensor with slicing before `torch.cat`.

## Explanation

The offsets are integers, so a centered crop keeps the feature alignment within one pixel.
