---
name: research-aae-prior-sample
title: 'Adversarial Autoencoders: Sampling the Prior'
tags: [research-papers, unsupervised, autoencoders, adversarial]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The adversarial autoencoder matches the distribution of its latent codes to a prior it can sample from. The prior here is a standard normal, and drawing samples from it is the first step of generating new data.

### From theory to code

Implement `prior_sample(rng, n, d)`, returning `n` standard normal samples of dimension `d`.

### Constraints

- Use the supplied `rng` for reproducibility.

### Hints

<details>
<summary>Hint 1</summary>

Call `rng.standard_normal` with shape `(n, d)`.

</details>

## Theory

### The simple version

Generation in an AAE starts from a prior sample, decodes it, and gets an image. Matching the codes to this prior is what makes those samples meaningful.

### The formula

$$z \sim p(z) = \mathcal{N}(0, I)$$

### How NumPy/PyTorch actually implements this

`torch.randn(n, d)` produces the same samples in PyTorch.

## Explanation

The code is a simple draw; the adversarial training is what makes the encoder's codes look like these samples.
