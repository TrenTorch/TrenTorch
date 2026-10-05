---
name: research-ldm-compression-ratio
title: 'Latent Diffusion: The Compression Ratio'
tags: [research-papers, computer-vision, diffusion, latent]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The point of latent diffusion is compression: the model works on far fewer numbers than the pixels. This ratio measures how much smaller the latent is than the image it encodes.

### From theory to code

Implement `compression_ratio(h, w, c_img, f, c_lat)`, the number of image values divided by the number of latent values.

### Constraints

- Returns a Python float.

### Hints

<details>
<summary>Hint 1</summary>

Count the image values, count the latent values with the latent grid size, and divide.

</details>

## Theory

### The simple version

A ratio of 48 means the diffusion model handles 48 times fewer values, which is the source of the speed-up. Too much compression would lose detail, which is the trade-off the autoencoder tunes.

### The formula

$$\rho = \frac{H\,W\,C_{\text{img}}}{\lfloor H/f\rfloor\,\lfloor W/f\rfloor\,C_{\text{lat}}}$$

### How NumPy/PyTorch actually implements this

Latent diffusion configs list the downsampling factor and latent channels, and this ratio follows from them.

## Explanation

The paper's experiments compare several factors and latent channel counts, reporting this ratio for each.
