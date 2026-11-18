---
name: research-vit-num-patches
title: 'ViT: Counting Image Patches'
tags: [research-papers, computer-vision, transformer, vision]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The Vision Transformer (Dosovitskiy et al., 2021) cuts an image into fixed-size patches and treats each patch as a token. The number of tokens, and hence the cost of attention, follows directly from the image size and patch size.

### From theory to code

Implement `num_patches(img, p)`, the number of patches for a square image.

### Constraints

- Use integer division.

### Hints

<details>
<summary>Hint 1</summary>

Divide the side length by the patch size, floor, then square.

</details>

## Theory

### The simple version

Doubling the image side quadruples the token count, which is why ViT cost grows quickly with resolution.

### The formula

$$N = \left(\frac{H}{P}\right)^2$$

### How NumPy/PyTorch actually implements this

`timm` ViT models compute this grid from the image and patch size in their embedding layer.

## Explanation

The 16 by 16 patch size gives 196 tokens for a 224 image, the setting the paper reports as ViT-B/16.
