---
name: vision-ddim-sampling-step
title: DDIM Sampling
tags: [diffusion, generative-models, sampling]
difficulty: Advanced
---

## Statement

### The problem, from first principles

DDPM needs about a thousand network evaluations per image. **DDIM** observes that the training objective does not depend on the forward process being Markov, which allows a family of samplers that are **deterministic** and can **skip steps**. A DDIM step first uses the noise prediction to estimate the clean image, `x0_hat`, and then re-noises that estimate to the _target_ noise level `t_prev` with the _same_ predicted noise: `x_prev = sqrt(ab_prev) * x0_hat + sqrt(1 - ab_prev) * eps_pred`. With `t_prev` far from `t`, a few dozen steps replace a thousand, and because no fresh noise is injected the same starting noise always gives the same image.

### From theory to code

Implement `ddim_step`.

### Constraints

- `ddim_step(x_t, eps_pred, t, t_prev, alpha_bars)`: `t` and `t_prev` are 0-based indices into `alpha_bars` with `t_prev < t`; `t_prev = -1` means the fully clean level `ab_prev = 1`.
- Compute `ab = alpha_bars[t]`, `x0_hat = (x_t - sqrt(1 - ab) * eps_pred) / sqrt(ab)`, then return `sqrt(ab_prev) * x0_hat + sqrt(1 - ab_prev) * eps_pred`.
- This is the `eta = 0` (deterministic) DDIM update.

### Hints

<details>
<summary>Hint 1</summary>

When `t_prev = -1`, `ab_prev = 1` so the result is exactly `x0_hat`.

</details>

<details>
<summary>Hint 2</summary>

If `eps_pred` is the true noise, the result equals the forward-process sample at `t_prev` built from the same noise.

</details>

## Theory

### The simple version

The map from a clean image to its noised version at any level is a straight path indexed by noise level. DDIM walks that path from one noise level to another by following the same direction (the predicted noise), so it can take big strides.

### The formula

$$
\hat x_0 = \frac{x_t - \sqrt{1 - \bar\alpha_t}\,\hat\epsilon}{\sqrt{\bar\alpha_t}}, \qquad
x_{t'} = \sqrt{\bar\alpha_{t'}}\,\hat x_0 + \sqrt{1 - \bar\alpha_{t'}}\,\hat\epsilon
$$

A nonzero $\eta$ adds back controlled noise and interpolates between DDIM ($\eta = 0$) and DDPM ($\eta = 1$).

### How this is done in practice

`diffusers`' `DDIMScheduler` and the 20 to 50 step default of Stable Diffusion pipelines use this idea. Faster solvers (DPM-Solver, UniPC) treat sampling as an ODE and use higher-order updates, but the first-order step is exactly DDIM.

## Explanation

The step is two lines. The most informative test is the consistency property: with the true noise, jumping several steps at once lands exactly where the forward process would have put the image.
