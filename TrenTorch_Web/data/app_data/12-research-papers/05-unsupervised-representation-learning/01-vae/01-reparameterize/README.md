---
name: research-vae-reparameterize
title: 'VAE: The Reparameterization Trick'
tags: [research-papers, unsupervised, vae, latent-variables]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A variational autoencoder encodes each input as a distribution, then samples a latent code from it. Sampling blocks gradients, so the paper rewrites the sample as a deterministic function of the parameters plus independent noise.

### From theory to code

Implement `reparameterize(mu, logvar, eps)`, returning `mu + exp(0.5 logvar) * eps`.

### Constraints

- Work with `logvar`, not the variance, for numerical stability.

### Hints

<details>
<summary>Hint 1</summary>

The standard deviation is `exp(0.5 * logvar)`. Scale the noise by it and add the mean.

</details>

## Theory

### The simple version

All randomness lives in `eps`, which does not depend on the parameters. The sample is then a smooth function of `mu` and `logvar`, so backpropagation works.

### The formula

$$z = \mu + \sigma \odot \epsilon, \qquad \epsilon \sim \mathcal{N}(0, I), \quad \sigma = \exp(\tfrac{1}{2}\log\sigma^2)$$

### How NumPy/PyTorch actually implements this

`torch.randn_like(std)` supplies `eps`; the expression is what the VAE implementations compute.

## Explanation

Writing the variance through its log keeps it positive without a constraint.
