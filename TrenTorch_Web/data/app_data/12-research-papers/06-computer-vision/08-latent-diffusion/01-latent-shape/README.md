---
name: research-ldm-latent-shape
title: 'Latent Diffusion: The Latent Grid Size'
tags: [research-papers, computer-vision, diffusion, latent]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Latent Diffusion (Rombach et al., 2022) runs the diffusion process in the compressed latent space of an autoencoder rather than on full-resolution pixels. A factor-8 autoencoder turns a 512 image into a 64 by 64 latent grid.

### From theory to code

Implement `latent_shape(h, w, f)`, the spatial size of the latent after downsampling by `f`.

### Constraints

- Integer division.

### Hints

<details>
<summary>Hint 1</summary>

Floor-divide each side by the factor.

</details>

## Theory

### The simple version

The diffusion model works on a grid that is 64 times smaller than the pixel count, so training and sampling are much cheaper at high resolution.

### The formula

$$(h', w') = \left(\left\lfloor\tfrac{h}{f}\right\rfloor, \left\lfloor\tfrac{w}{f}\right\rfloor\right)$$

### How NumPy/PyTorch actually implements this

Stable Diffusion's VAE uses factor 8, so a 512 pixel image becomes a 64 by 64 latent, exactly this formula.

## Explanation

The factor f is the autoencoder's total spatial downsampling, set by its stride stack.
