---
name: research-gan-generator-loss
title: 'GAN: The Non-saturating Generator Loss'
tags: [research-papers, unsupervised, gan, generative-models]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The original generator loss, log(1 - D(G(z))), saturates when the discriminator is confident, leaving the generator with almost no gradient. The paper's non-saturating variant maximizes log D(G(z)) instead, which gives a strong signal early in training.

### From theory to code

Implement `gan_generator_loss(d_fake)`, returning `-mean(log D(G(z)))`.

### Constraints

- Returns a Python float.

### Hints

<details>
<summary>Hint 1</summary>

Take the log of the discriminator's output on fake samples, average, and negate.

</details>

## Theory

### The simple version

When the discriminator rejects fakes, D is near zero and log(1 - D) has a flat slope. The non-saturating form has a steep slope exactly in that case.

### The formula

$$L_G = -\mathbb{E}_{z}[\log D(G(z))]$$

### How NumPy/PyTorch actually implements this

DCGAN and most GAN code use this form for the generator loss.

## Explanation

The two generator objectives share the same fixed point, but this one gives useful gradients when the generator is losing.
