---
name: research-vae-kl
title: 'VAE: The KL to the Prior'
tags: [research-papers, unsupervised, vae, latent-variables]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The VAE objective includes a KL term that pulls each posterior toward a standard normal prior. This keeps the latent space smooth, so random samples from the prior decode to plausible data.

### From theory to code

Implement `kl_std_normal(mu, logvar)`, the KL from a diagonal Gaussian to the standard normal, summed over dimensions.

### Constraints

- Sum over dimensions and return a Python float.

### Hints

<details>
<summary>Hint 1</summary>

Use `-0.5 * sum(1 + logvar - mu^2 - exp(logvar))`.

</details>

## Theory

### The simple version

The KL is zero exactly when the posterior equals the prior, and it grows with the mean's distance from zero and the variance's distance from one.

### The formula

$$D_{\text{KL}} = -\frac{1}{2}\sum_j\big(1 + \log\sigma_j^2 - \mu_j^2 - \sigma_j^2\big)$$

### How NumPy/PyTorch actually implements this

`torch.distributions.kl_divergence` gives the same value for Normal distributions.

## Explanation

This closed form is why the VAE needs no sampling to compute its regularizer.
