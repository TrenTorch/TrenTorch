---
name: vision-forward-diffusion
title: Forward Diffusion
tags: [diffusion, generative-models, forward-process]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Adding noise one step at a time would make training painfully slow, since producing a noisy image for step 500 would need 500 sequential operations. But Gaussian noise has a convenient property: the sum of Gaussians is Gaussian. Composing all the steps gives a **closed form** that jumps from the clean image `x0` straight to step `t`: `x_t = sqrt(alpha_bar_t) * x0 + sqrt(1 - alpha_bar_t) * eps` with `eps ~ N(0, I)`. This is a weighted blend of signal and noise whose weights satisfy `a^2 + b^2 = 1`, so if `x0` has unit variance then so does `x_t`. The **signal-to-noise ratio** `alpha_bar / (1 - alpha_bar)` summarizes how corrupted the image is at each step.

### From theory to code

Implement `q_sample` and `snr`.

### Constraints

- `q_sample(x0, t, alpha_bars, noise)` returns `sqrt(alpha_bars[t]) * x0 + sqrt(1 - alpha_bars[t]) * noise`. `t` is a 0-based integer index into `alpha_bars`; `x0` and `noise` have the same shape.
- `snr(alpha_bars)` returns `alpha_bars / (1 - alpha_bars)` as an array (assume `alpha_bars < 1`).
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

The noise is supplied as an argument so the function is deterministic, which also mirrors training where the same noise is the regression target.

</details>

<details>
<summary>Hint 2</summary>

At `alpha_bar` near 1 the output is almost `x0`, near 0 it is almost `noise`.

</details>

## Theory

### The simple version

Mixing a photo with static on a TV: turn the dial and you get a precisely weighted blend, with the weights chosen so the overall brightness of the picture-plus-static stays the same.

### The formula

$$
x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1 - \bar\alpha_t}\,\epsilon, \qquad \epsilon \sim \mathcal{N}(0, I), \qquad \text{SNR}(t) = \frac{\bar\alpha_t}{1 - \bar\alpha_t}
$$

$\text{Var}(x_t) = \bar\alpha_t \text{Var}(x_0) + (1 - \bar\alpha_t)$, which equals 1 when $\text{Var}(x_0) = 1$.

### How this is done in practice

This is `q(x_t | x_0)` from the DDPM paper and the first line of every diffusion training loop: sample a random `t`, sample noise, build `x_t`, ask the network to recover the noise. Because SNR falls monotonically with `t`, some training objectives weight timesteps by SNR.

## Explanation

A single blend of the clean data and noise. The statistical tests (variance preserved, endpoints, SNR monotone) are the properties that make the closed form trustworthy.
