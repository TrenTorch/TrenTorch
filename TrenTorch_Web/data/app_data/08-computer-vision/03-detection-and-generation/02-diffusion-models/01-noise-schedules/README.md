---
name: vision-noise-schedules
title: Noise Schedules
tags: [diffusion, generative-models, schedules]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A diffusion model learns to reverse a slow process that destroys an image with noise. The forward process adds a little Gaussian noise at each of `T` steps, controlled by a **variance schedule** `beta_t`. Because the steps compose, there is a closed form for the total effect after `t` steps, governed by the cumulative product `alpha_bar_t = prod_{s<=t} (1 - beta_s)`: it starts near 1 (almost all signal) and decays toward 0 (almost all noise). The shape of the schedule matters. The original **linear** schedule destroys information too quickly near the end, wasting many steps on pure noise. The **cosine** schedule defines `alpha_bar` directly with a smooth cosine curve, so the signal decays gently at both ends.

### From theory to code

Implement `linear_betas`, `alpha_bars` and `cosine_alpha_bars`.

### Constraints

- `linear_betas(T, beta_start, beta_end)` returns `T` values spaced evenly from `beta_start` to `beta_end` inclusive (`np.linspace`).
- `alpha_bars(betas)` returns `np.cumprod(1 - betas)`.
- `cosine_alpha_bars(T, s=0.008)` returns `alpha_bar[t] = f(t + 1) / f(0)` for `t = 0..T-1` (so `T` values) where `f(u) = cos(((u / T) + s) / (1 + s) * pi / 2) ** 2`.
- All return NumPy float arrays.

### Hints

<details>
<summary>Hint 1</summary>

`alpha_bars` is a one-line cumulative product.

</details>

<details>
<summary>Hint 2</summary>

In the cosine schedule `f(0)` normalizes the curve so the signal fraction starts near 1.

</details>

## Theory

### The simple version

A message passed down a line of people who each garble it slightly: the schedule says how much each person garbles it, and `alpha_bar` is how much of the original message survives after `t` people.

### The formula

$$
\bar\alpha_t = \prod_{s=1}^{t}(1 - \beta_s), \qquad
\bar\alpha_t^{\cos} = \frac{f(t)}{f(0)},\quad f(t) = \cos^2\!\Big(\frac{t/T + s}{1 + s}\cdot\frac{\pi}{2}\Big)
$$

### How this is done in practice

DDPM used a linear schedule from `1e-4` to `0.02` over 1000 steps. Nichol and Dhariwal's improved DDPM introduced the cosine schedule, and modern models additionally rescale schedules to have zero terminal signal-to-noise ratio, which matters for very bright or dark images.

## Explanation

The cumulative product is the object everything else in the diffusion pipeline uses. The tests check the two schedules against their defining properties: monotone decrease, start near 1 and decay toward 0.
