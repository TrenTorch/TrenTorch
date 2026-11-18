---
name: research-aae-encoder-loss
title: 'Adversarial Autoencoders: The Encoder's Adversarial Loss'
tags: [research-papers, unsupervised, autoencoders, adversarial]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

In the AAE the encoder plays the generator's role in the adversarial game: it tries to make its codes look like prior samples to the discriminator. The loss is the same non-saturating form as a GAN generator loss.

### From theory to code

Implement `encoder_fooling_loss(d_codes)`, returning `-mean(log D(z))` over the encoder's codes.

### Constraints

- Returns a Python float.

### Hints

<details>
<summary>Hint 1</summary>

Take the log of the discriminator outputs on codes, average, and negate.

</details>

## Theory

### The simple version

Training pushes the encoder toward codes the discriminator scores as prior samples. Combined with the reconstruction loss, this keeps codes both informative and well-distributed.

### The formula

$$\mathcal{L}_{\text{enc}} = -\mathbb{E}_{x}[\log D(E(x))]$$

### How NumPy/PyTorch actually implements this

AAE training alternates a discriminator step on prior samples and encoder codes with an encoder step using this loss.

## Explanation

This is the GAN generator objective with the encoder in the role of the generator.
