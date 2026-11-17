---
name: research-ddpm-forward-noise
title: 'DDPM: Adding Noise in One Step'
tags: [research-papers, computer-vision, diffusion, generative-models]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A diffusion model learns to reverse a gradual noising process. The paper's key identity lets you jump from the clean image to any noise level in one step, without simulating each intermediate step.

### From theory to code

Implement `forward_noise(x0, ab, eps)`, the closed-form noised sample at a given noise level.

### Constraints

- `ab` is the cumulative signal fraction, between 0 and 1.

### Hints

<details>
<summary>Hint 1</summary>

Scale the clean sample by the square root of `ab` and the noise by the square root of `1 - ab`, then add.

</details>

## Theory

### The simple version

The two weights sum in quadrature to one, so the variance is preserved: noise and signal trade off smoothly as `ab` decreases.

### The formula

$$x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1 - \bar\alpha_t}\,\epsilon$$

### How NumPy/PyTorch actually implements this

DDPM training draws a random `t` per sample and computes this noisy input in one line.

## Explanation

The closed form follows from composing the Gaussian transitions of the forward chain.
