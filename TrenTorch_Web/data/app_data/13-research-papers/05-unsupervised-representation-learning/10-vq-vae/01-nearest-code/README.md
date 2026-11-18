---
name: research-vq-nearest-code
title: 'VQ-VAE: Choosing the Nearest Code'
tags: [research-papers, unsupervised, discrete-latents, vae]
difficulty: Beginner
---

## Statement

### The problem, from first principles

VQ-VAE (van den Oord et al., 2017) quantizes each encoder output to its nearest entry in a learned codebook. The latent becomes a discrete index, which the decoder maps back to a code vector.

### From theory to code

Implement `nearest_code_index(z, codebook)`, the index of the closest codebook row.

### Constraints

- Distance is Euclidean; ties go to the first index.

### Hints

<details>
<summary>Hint 1</summary>

Compute the distances from `z` to every code and take the argmin.

</details>

## Theory

### The simple version

The discrete choice is the bottleneck: the decoder sees only which code was picked. Learning the codebook makes those choices informative.

### The formula

$$k = \arg\min_j \lVert z_e(x) - e_j\rVert_2$$

### How NumPy/PyTorch actually implements this

VQ-VAE implementations find the nearest code with a broadcast distance matrix and `argmin`.

## Explanation

The argmin is non-differentiable, so the paper passes the gradient straight through the quantization step.
