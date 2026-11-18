---
name: vision-noise-prediction-loss
title: Noise Prediction Loss
tags: [diffusion, generative-models, training]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

DDPM turns generation into a regression problem. Take a clean image, pick a random step `t`, draw noise `eps`, form the noisy image `x_t`, and train a network `eps_theta(x_t, t)` to predict the noise that was added. The loss is the mean squared error between the predicted and the true noise. Predicting the noise is mathematically equivalent to predicting the clean image: because `x_t = sqrt(ab) * x0 + sqrt(1 - ab) * eps`, rearranging gives `x0 = (x_t - sqrt(1 - ab) * eps) / sqrt(ab)`. So any noise prediction implies an estimate of the clean image, which is what sampling algorithms use at every step.

### From theory to code

Implement `noise_prediction_loss` and `predict_x0`.

### Constraints

- `noise_prediction_loss(eps_pred, eps)` is the mean over all elements of `(eps_pred - eps) ** 2`, as a Python float.
- `predict_x0(x_t, eps_pred, t, alpha_bars)` returns `(x_t - sqrt(1 - ab) * eps_pred) / sqrt(ab)` with `ab = alpha_bars[t]` (0-based index).
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

If `eps_pred` equals the true noise, `predict_x0` must return the original clean image exactly.

</details>

<details>
<summary>Hint 2</summary>

A model that always predicts zero noise has loss equal to the variance of the noise, about 1.

</details>

## Theory

### The simple version

The network is a detective given a smudged photo and asked to describe the smudge. If it can describe the smudge perfectly, wiping it off reveals the original.

### The formula

$$
\mathcal{L} = \mathbb{E}_{x_0, t, \epsilon}\,\big\lVert \epsilon - \epsilon_\theta(x_t, t)\big\rVert^2, \qquad
\hat x_0 = \frac{x_t - \sqrt{1 - \bar\alpha_t}\,\hat\epsilon}{\sqrt{\bar\alpha_t}}
$$

### How this is done in practice

This simple loss trains Stable Diffusion's U-Net and most image generators. Variants predict `x0` or the velocity `v = sqrt(ab) eps - sqrt(1 - ab) x0` instead, which behave better at the extremes of the schedule. Clamping the predicted `x0` to the valid pixel range is a common stabilization when sampling.

## Explanation

The loss is an MSE and the conversion is algebra, but the pair shows the key equivalence between the three common parametrizations, with the test that a perfect noise prediction recovers the exact image.
