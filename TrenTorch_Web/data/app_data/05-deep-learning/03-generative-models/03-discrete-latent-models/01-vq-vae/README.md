---
name: dl-generative-vq-vae
title: Vector Quantized Variational Autoencoder
tags: [deep-learning, generative-models, vq-vae]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

VQ-VAE learns discrete latent codes by quantizing continuous latent representations. An encoder maps input to a continuous space, which is quantized to the nearest code in a learned codebook. A decoder reconstructs from the quantized code.

Loss combines reconstruction, codebook, and commitment terms:
$$\mathcal{L} = ||x - \hat{x}||^2 + ||sg[z_e] - e||^2 + \beta||z_e - sg[e]||^2$$

Where sg denotes stop-gradient, z_e is the encoder output, and e is the quantized code.

### From theory to code

Implement:

```python
vq_vae_loss(x_recon, x_true, z_e, z_q, beta=0.25)
```

Computes reconstruction, codebook, and commitment losses.

### Constraints

- x_recon, x_true shape: (N, D)
- z_e (encoder), z_q (quantized) shape: (N, D)
- beta: commitment loss weight (default 0.25).
- Return scalar loss.

## Theory

VQ-VAE maps continuous representations to discrete codes, learning useful quantized latent spaces. Useful for hierarchical generation and discrete variable learning.

## Explanation

Reconstruction loss: MSE. Codebook loss: MSE between stop-grad encoder and codes. Commitment loss: encourages encoder to commit to close codes.
