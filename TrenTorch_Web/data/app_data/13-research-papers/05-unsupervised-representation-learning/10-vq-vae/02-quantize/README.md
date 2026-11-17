---
name: research-vq-quantize
title: 'VQ-VAE: Looking Up the Code'
tags: [research-papers, unsupervised, discrete-latents, vae]
difficulty: Beginner
---

## Statement

### The problem, from first principles

After the nearest code is chosen, the quantized latent is simply that code vector. The decoder receives the code, so the index is all it needs to reconstruct the image.

### From theory to code

Implement `quantize(codebook, idx)`, which returns the code vectors at the given indices.

### Constraints

- Works for one index or many.

### Hints

<details>
<summary>Hint 1</summary>

Index the codebook with `idx`.

</details>

## Theory

### The simple version

Quantization is a table lookup. Because the codebook is small and discrete, the whole latent can be stored as a grid of integers.

### The formula

$$z_q(x) = e_k, \qquad k = \arg\min_j \lVert z_e(x) - e_j\rVert$$

### How NumPy/PyTorch actually implements this

VQ-VAE decoders call `codebook[indices]` on the stored latent grid.

## Explanation

This is the forward pass of the quantizer; the straight-through estimator handles the backward pass.
