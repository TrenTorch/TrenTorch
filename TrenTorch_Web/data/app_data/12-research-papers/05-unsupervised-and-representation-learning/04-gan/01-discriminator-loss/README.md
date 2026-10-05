---
name: research-gan-discriminator-loss
title: 'GAN: The Discriminator Loss'
tags: [research-papers, unsupervised, gan, generative-models]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A GAN (Goodfellow et al., 2014) trains a discriminator to tell real samples from generated ones. The discriminator's loss is the binary cross-entropy: score real data high and generated data low.

### From theory to code

Implement `gan_discriminator_loss(d_real, d_fake)`, the sum of the two cross-entropy means.

### Constraints

- Outputs are probabilities strictly between 0 and 1.

### Hints

<details>
<summary>Hint 1</summary>

Average `-log D` over real samples and `-log(1 - D)` over fake ones, then add.

</details>

## Theory

### The simple version

At chance (outputs 0.5) the loss is 2 log 2, the baseline the game starts from. A discriminator that separates the two groups drives the loss toward zero.

### The formula

$$L_D = -\mathbb{E}_{x\sim p_{\text{data}}}[\log D(x)] - \mathbb{E}_{z}[\log(1 - D(G(z)))]$$

### How NumPy/PyTorch actually implements this

Training scripts often use `BCEWithLogitsLoss` on the discriminator logits, which computes the same objective stably.

## Explanation

This is the standard binary cross-entropy with real labelled one and fake labelled zero.
