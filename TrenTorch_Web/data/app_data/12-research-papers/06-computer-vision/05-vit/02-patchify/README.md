---
name: research-vit-patchify
title: 'ViT: Patchifying an Image'
tags: [research-papers, computer-vision, transformer, vision]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A ViT treats an image as a sequence of patch tokens. Each patch is flattened into a vector before a linear projection, so the layout of the patches has to be set up carefully.

### From theory to code

Implement `patchify(img, p)`, which splits the image into flattened non-overlapping patches.

### Constraints

- Patches are listed row by row.

### Hints

<details>
<summary>Hint 1</summary>

Reshape to a grid of blocks, move the grid axes to the front, then flatten each block.

</details>

## Theory

### The simple version

Each patch keeps all its pixels, and the patch order gives the transformer the spatial layout that positional embeddings then encode.

### The formula

$$x \in \mathbb{R}^{H\times W} \;\longrightarrow\; \{x_i \in \mathbb{R}^{P^2}\}_{i=1}^{N}$$

### How NumPy/PyTorch actually implements this

The patch embedding in ViT is a convolution with stride equal to the patch size, which computes the same flattened patches.

## Explanation

The reshape and transpose are the same pattern used for splitting attention heads, here applied to spatial blocks.
