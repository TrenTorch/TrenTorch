---
name: vision-ddpm-sampling-step
title: DDPM Reverse Sampling
tags: [diffusion, generative-models, sampling]
difficulty: Advanced
---

## Statement

### The problem, from first principles

To generate an image, start from pure noise `x_T` and denoise one step at a time, from `T` down to 1. A **DDPM reverse step** takes the current noisy image `x_t`, asks the network for its noise estimate, and computes the mean of a Gaussian over the slightly less noisy `x_{t-1}`. The mean subtracts the predicted noise, scaled by a factor that depends on the schedule: `mu = (x_t - beta_t / sqrt(1 - ab_t) * eps) / sqrt(alpha_t)` where `alpha_t = 1 - beta_t`. Then a bit of fresh Gaussian noise with standard deviation `sqrt(beta_t)` is added back, except at the very last step where the output should be the clean sample. That injected noise makes DDPM sampling stochastic.

### From theory to code

Implement `ddpm_step`.

### Constraints

- `ddpm_step(x_t, eps_pred, t, betas, alpha_bars, z)` uses 0-based `t` (index into `betas` and `alpha_bars`), with `alpha_t = 1 - betas[t]`.
- The mean is `mu = (x_t - betas[t] / sqrt(1 - alpha_bars[t]) * eps_pred) / sqrt(alpha_t)`.
- If `t > 0` return `mu + sqrt(betas[t]) * z`. If `t == 0` return `mu` with no noise added.
- `z` is standard Gaussian noise of the same shape as `x_t`, passed in so the step is deterministic.

### Hints

<details>
<summary>Hint 1</summary>

Compute the mean first, then decide whether to add noise.

</details>

<details>
<summary>Hint 2</summary>

The noise at the last step is omitted because adding noise to the final image would only degrade it.

</details>

## Theory

### The simple version

Restoring a damaged painting a bit at a time: each pass removes the amount of damage the restorer believes was added in the latest layer, then a tiny deliberate jitter keeps the process from collapsing to one single outcome.

### The formula

$$
x_{t-1} = \frac{1}{\sqrt{\alpha_t}}\Big(x_t - \frac{\beta_t}{\sqrt{1 - \bar\alpha_t}}\,\epsilon_\theta(x_t, t)\Big) + \sigma_t z, \qquad \sigma_t = \sqrt{\beta_t},\; z \sim \mathcal{N}(0, I)
$$

with $z = 0$ at the final step.

### How this is done in practice

This is Algorithm 2 of the DDPM paper. Libraries such as `diffusers` implement it in `DDPMScheduler.step`, with options for the variance (fixed small, fixed large, learned) and for clipping the predicted `x0`. A thousand sequential network calls make it slow, which motivated deterministic samplers such as DDIM.

## Explanation

Algebra on arrays plus one branch. The consistency test, that the mean computed from the true noise matches the true posterior mean, links this step back to the forward process.
