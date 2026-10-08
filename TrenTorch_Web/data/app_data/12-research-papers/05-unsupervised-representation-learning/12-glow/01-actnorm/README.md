---
name: research-glow-actnorm
title: 'Glow: Activation Normalization'
tags: [research-papers, unsupervised, normalizing-flows, generative-models]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Glow (Kingma & Dhariwal, 2018) is a normalizing flow: an invertible chain of transformations from data to a simple base distribution. Activation normalization is the first step, a per-channel affine map whose parameters are initialized from data.

### From theory to code

Implement `actnorm_forward(x, scale, bias)`, returning `(x + bias) * scale` per channel.

### Constraints

- Channels are the last axis.

### Hints

<details>
<summary>Hint 1</summary>

Add the bias, then multiply by the scale; NumPy broadcasts over the channel axis.

</details>

## Theory

### The simple version

The map is invertible whenever the scale is nonzero, which is what a flow requires. Its log-determinant is needed for the likelihood, and the next questions compute it.

### The formula

$$y = (x + b)\odot s$$

### How NumPy/PyTorch actually implements this

Glow's ActNorm layer is this affine map plus a log-determinant term for each spatial position.

## Explanation

The per-channel scale and bias are learned like batch norm parameters but initialized from the first mini-batch.
