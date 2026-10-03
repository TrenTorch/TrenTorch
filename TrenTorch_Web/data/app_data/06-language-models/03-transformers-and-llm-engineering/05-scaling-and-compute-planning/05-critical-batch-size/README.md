---
name: lm-critical-batch-size
title: Critical Batch Size & Gradient Noise
tags: [scaling-laws, batch-size, optimization]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Doubling the batch size does not always halve the number of steps. Small batches have noisy gradients, so averaging more examples helps a lot. Past a point the gradient is already accurate and extra examples only cost compute. The turning point is the **critical batch size**, and it can be estimated from gradients you already compute. The **gradient noise scale** is the ratio of the total variance of per-example gradients to the squared length of their mean: noise over signal. When the batch is much smaller than this ratio, steps are noise-dominated and a bigger batch helps nearly linearly. When it is much larger, steps are signal-dominated and a bigger batch barely helps.

### From theory to code

Implement `gradient_noise_scale` and `steps_to_target`.

### Constraints

- `per_example_grads` has shape `(n, d)`, one gradient vector per example, `n >= 2`.
- `gradient_noise_scale(per_example_grads)` returns `trace_sigma / ||g_mean||**2` where `g_mean` is the mean gradient and `trace_sigma = sum over examples of ||g_i - g_mean||**2 / (n - 1)` (the unbiased trace of the covariance).
- `steps_to_target(batch_size, s_min, b_crit)` is `s_min * (1 + b_crit / batch_size)`, the number of steps needed to reach a fixed loss at that batch size.
- Return Python floats.

### Hints

<details>
<summary>Hint 1</summary>

Use `ddof=1`-style normalization: divide the summed squared deviations by `n - 1`.

</details>

<details>
<summary>Hint 2</summary>

At a batch size equal to `b_crit` the step count is `2 * s_min`.

</details>

## Theory

### The simple version

Polling opinion: asking ten people gives a noisy answer, asking a thousand a good one, asking a million adds little. The noise scale says where on that curve you are.

### The formula

$$
\mathcal{B}_{\text{noise}} = \frac{\operatorname{tr}\Sigma}{\lVert G\rVert^2}, \qquad S(B) = S_{\min}\Big(1 + \frac{B_{\text{crit}}}{B}\Big)
$$

Steps fall like $1/B$ for $B \ll B_{\text{crit}}$ and flatten at $S_{\min}$ for $B \gg B_{\text{crit}}$, while the total examples processed $E = S\,B$ grows linearly in $B$ once past the knee.

### How this is done in practice

McCandlish et al. ("An Empirical Model of Large-Batch Training") introduced the noise scale. Labs measure it during training, since it grows as the loss falls, which is why batch size is increased during long runs. The plug-in estimate here is biased when `n` is small, and papers use unbiased two-batch estimators.

## Explanation

The estimator is two lines of NumPy. The step-count model turns the number into a decision: at `B = B_crit` you use twice the minimum steps and twice the minimum examples.
