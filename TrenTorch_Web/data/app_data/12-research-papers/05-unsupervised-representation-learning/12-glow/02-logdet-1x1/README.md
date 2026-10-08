---
name: research-glow-logdet-1x1
title: 'Glow: The Log-determinant of an Invertible 1x1 Convolution'
tags: [research-papers, unsupervised, normalizing-flows, generative-models]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Glow's invertible 1x1 convolution mixes channels with a learned square matrix at every spatial position. Its contribution to the change-of-variables formula is the log-determinant, which scales with the number of positions.

### From theory to code

Implement `logdet_1x1(W, h, w)`, returning `h * w * log|det W|`.

### Constraints

- Use `slogdet` for stability.

### Hints

<details>
<summary>Hint 1</summary>

Compute the log absolute determinant with `slogdet`, then multiply by the number of spatial positions.

</details>

## Theory

### The simple version

The determinant measures how much the layer stretches volume. Log-determinants add across layers, so the total likelihood correction is a sum of simple terms.

### The formula

$$\log\left|\det \frac{\partial y}{\partial x}\right| = h\,w\,\log|\det W|$$

### How NumPy/PyTorch actually implements this

Glow implementations compute the determinant with an LU decomposition, which is cheaper than a full determinant for large channel counts.

## Explanation

Each spatial position is transformed by the same matrix, so the Jacobian is block diagonal with W repeated h times w.
