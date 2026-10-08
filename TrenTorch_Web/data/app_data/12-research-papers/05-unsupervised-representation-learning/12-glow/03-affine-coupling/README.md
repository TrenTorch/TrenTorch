---
name: research-glow-affine-coupling
title: 'Glow: The Affine Coupling Layer'
tags: [research-papers, unsupervised, normalizing-flows, generative-models]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Glow's affine coupling layer splits the features in two. One half passes through unchanged and is used to compute a scale and shift for the other half. Because the first half is known, the transform can be inverted exactly.

### From theory to code

Implement `affine_coupling_forward(xa, xb, s, t)`, returning the unchanged half and the scaled and shifted half.

### Constraints

- `s` is a log-scale, so the scale factor is `exp(s)`.

### Hints

<details>
<summary>Hint 1</summary>

Keep `xa` as is, and compute `xb * exp(s) + t`.

</details>

## Theory

### The simple version

Because the scale comes from the unchanged half, the inverse is simple: subtract the shift and divide by the scale. This invertibility is what makes the flow usable for exact likelihoods.

### The formula

$$y_a = x_a,\qquad y_b = x_b \odot \exp\big(s(x_a)\big) + t(x_a)$$

### How NumPy/PyTorch actually implements this

Glow's coupling layer uses a small convolutional network to compute `s` and `t` from the first half.

## Explanation

The log-determinant of this map is the sum of the log-scales, so the likelihood correction is cheap to compute.
