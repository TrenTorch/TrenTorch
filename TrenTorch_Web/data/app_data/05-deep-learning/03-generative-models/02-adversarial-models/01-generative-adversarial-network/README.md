---
name: dl-generative-gan
title: Generative Adversarial Network
tags: [deep-learning, generative-models, gan]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A Generative Adversarial Network (GAN) consists of a generator G that produces fake samples and a discriminator D that distinguishes fake from real. They are trained in an adversarial game where D tries to maximize accuracy and G tries to fool D.

$$\min_G \max_D \mathbb{E}_{x \sim p_{data}}[\log D(x)] + \mathbb{E}_{z \sim p_z}[\log(1 - D(G(z)))]$$

In practice, use binary cross-entropy loss for both networks.

### From theory to code

Implement:

```python
gan_loss(d_real_logits, d_fake_logits, is_discriminator=True)
```

Computes the loss for discriminator or generator training.

### Constraints

- d_real_logits shape: (N,)
- d_fake_logits shape: (N,)
- is_discriminator: bool flag for which loss to compute.
- Return scalar loss.

## Theory

GAN training is unstable but powerful. The game-theoretic formulation leads to the generator learning the data distribution at Nash equilibrium.

## Explanation

Discriminator loss: BCE for real (target 1) and fake (target 0) samples. Generator loss: BCE for fake samples with target 1 (trying to fool discriminator).
