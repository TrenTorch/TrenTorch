---
name: research-ddpm-linear-schedule
title: 'DDPM: The Linear Noise Schedule'
tags: [research-papers, computer-vision, diffusion, generative-models]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

DDPM uses a fixed schedule of noise levels. A linear schedule of small variances, accumulated as a cumulative product, gives the fraction of the original signal left at each step.

### From theory to code

Implement `alpha_bars(T, b0, b1)`, the cumulative product of `1 - beta_t` for a linear schedule from `b0` to `b1`.

### Constraints

- The schedule is linear in beta.

### Hints

<details>
<summary>Hint 1</summary>

Make `T` evenly spaced betas, subtract them from one, then take the running product.

</details>

## Theory

### The simple version

Early steps keep almost all of the signal, and late steps are nearly pure noise. The cumulative product is what the closed-form forward process needs.

### The formula

$$\beta_t = \beta_0 + \frac{t}{T-1}(\beta_1 - \beta_0), \qquad \bar\alpha_t = \prod_{s \le t}(1 - \beta_s)$$

### How NumPy/PyTorch actually implements this

Diffusion libraries precompute this array once and index it during training and sampling.

## Explanation

The schedule values are hyperparameters; the paper's linear schedule uses 1e-4 to 0.02 over 1000 steps.
