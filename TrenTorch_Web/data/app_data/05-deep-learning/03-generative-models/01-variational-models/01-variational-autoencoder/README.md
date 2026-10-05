---
name: dl-generative-vae
title: Variational Autoencoder
tags: [deep-learning, generative-models, vae]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A Variational Autoencoder (VAE) learns a probabilistic latent space representation. The encoder maps input x to mean/logvar of a Gaussian distribution. The decoder samples from this distribution to reconstruct x. The loss combines reconstruction (MSE/BCE) and KL divergence regularization.

$$\mathcal{L} = \mathbb{E}_{q_\phi(z|x)}[\log p_\psi(x|z)] - D_{KL}(q_\phi(z|x) || p(z))$$

Where q is the encoder, p is the decoder, and p(z) = N(0, I).

### From theory to code

Implement:

```python
vae_loss(x_recon, x_true, mu, logvar)
```

Computes the evidence lower bound (ELBO) loss for VAE training.

### Constraints

- x_recon, x_true shape: (N, D)
- mu, logvar shape: (N, latent_dim)
- Return scalar loss.
- Reconstruction loss is MSE.

## Theory

VAE learns a latent representation by maximizing the probability of data while keeping the latent distribution close to N(0, I). This enables generation by sampling from the prior.

## Explanation

Reconstruction loss is mean squared error over dimensions. KL divergence regularization is derived from Gaussian assumptions: KL = 0.5 * sum(-logvar - 1 + exp(logvar) + mu^2).
