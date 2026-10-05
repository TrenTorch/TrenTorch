---
name: research-vae-elbo
title: 'VAE: The Evidence Lower Bound'
tags: [research-papers, unsupervised, vae, latent-variables]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The VAE maximizes a lower bound on the log-likelihood of the data. The bound is the reconstruction term minus a KL penalty, and it can be estimated with samples from the posterior.

### From theory to code

Implement `elbo(log_px_given_z, kl)`, returning the reconstruction term minus the KL.

### Constraints

- The result is maximized; training minimizes its negative.

### Hints

<details>
<summary>Hint 1</summary>

Subtract the KL from the reconstruction log-likelihood.

</details>

## Theory

### The simple version

The bound is tight when the posterior matches the true posterior. Reconstruction rewards faithful encodings, and the KL term keeps them close to the prior.

### The formula

$$\log p(x) \ge \mathbb{E}_{q(z|x)}[\log p(x|z)] - D_{\text{KL}}\big(q(z|x)\,\|\,p(z)\big)$$

### How NumPy/PyTorch actually implements this

VAE training loops minimize `-elbo` per example, averaged over the batch.

## Explanation

The gap between the two sides is the KL from the approximate to the true posterior, which is why the bound improves as the posterior improves.
