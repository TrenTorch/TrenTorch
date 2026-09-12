---
name: dl-training-adam-bias-correction
title: 'Adam: bias-corrected moment estimates'
tags: [optimization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`SGD + Momentum` maintained one running average of gradients (velocity), initialized at zero. That zero initialization has a real, measurable cost right at the START of training: on the very first step, the running average is mostly still "zero, blended with a tiny sliver of real gradient," a systematic UNDERESTIMATE of the true gradient's actual scale. `SGD + Momentum` never corrects for this (it doesn't need to, in practice the effect is small and the optimizer isn't ALSO trying to divide by this quantity), but Adam, the next real optimizer this track builds toward, tracks two running averages, and specifically USES one of them (the squared-gradient average) as a DIVISOR in its update rule, which makes an early, zero-biased underestimate a genuinely serious problem: dividing by a falsely-small number early in training would produce a wildly oversized, unstable step.

This question builds Adam's fix in isolation, before the full update rule needs it: a precise correction formula that removes exactly the zero-initialization bias, self-adjusting so it matters a lot on step 1 and fades away naturally as training proceeds.

### From theory to code

Theory tracks two running averages, `m` (mean of the gradient) and `v` (mean of the SQUARED gradient), each updated with an exponential-moving-average formula, and derives an exact correction factor, `1 / (1 - beta^t)`, that removes the systematic zero-initialization bias at step `t`.

Implement `update_moments(m, v, grad, beta1=0.9, beta2=0.999)` first, then `bias_correct(moment, beta, t)`.

### Constraints

- `m` and `v` both start at `0.0` before the first call.
- `t` is 1-indexed: `t=1` is the very first update.
- `bias_correct` works identically for both `m` (with `beta1`) and `v` (with `beta2`), it's the same formula, only which moment and which beta differ.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`update_moments` is two exponential-moving-average updates, one for `grad`, one for `grad**2`, using `beta1` and `beta2` respectively.

</details>

<details>
<summary>Hint 2</summary>

`bias_correct(moment, beta, t)` is `moment / (1 - beta**t)`, a single division.

</details>

## Theory

### The simple version

A new employee's very first performance review, averaged in with zero prior history, looks artificially low, not because they're actually performing poorly, but because "one real data point, blended with a fictional starting point of zero" mathematically undersells them. After enough reviews accumulate, that fictional zero starting point barely matters anymore, the average is dominated by real data. Adam's moment estimates have exactly this problem at the start of training, and bias correction is the precise mathematical fix, scaling the early estimate up by exactly the right amount to cancel out that fictional-zero-starting-point effect.

### The formula

Two running averages, updated every step:

```text
m_new = beta1 * m + (1 - beta1) * grad         -- running average of the gradient
v_new = beta2 * v + (1 - beta2) * grad^2        -- running average of the squared gradient
```

Both start at `0`, which means, unrolled, `m` after `t` steps is actually a weighted average of the true gradients, but scaled DOWN by a factor of `(1 - beta1^t)` compared to what a true unbiased running average would be (a fact provable by expanding the recursive formula, not something this question asks you to derive, only to apply). The correction exactly undoes that scaling:

```text
bias_correct(moment, beta, t) = moment / (1 - beta^t)
```

On step `t=1`, `beta^1` is close to `beta` itself (e.g. `0.9` for `beta1`), so `1 - beta^1` is small, and the correction is a LARGE multiplier, exactly compensating for how dominated the very first raw moment estimate is by its zero starting point. As `t` grows, `beta^t -> 0` (since `beta < 1`), so `1 - beta^t -> 1`, and the correction fades to having essentially no effect, exactly when the running average has accumulated enough real data to no longer need it.

### How PyTorch actually implements this

`torch.optim.Adam` computes precisely these two running averages and applies precisely this bias correction internally, every single step, `Adam: full update rule` (the next question in this track) assembles them into the complete optimizer. Skipping bias correction (an option some Adam variants and reimplementations genuinely get wrong) produces measurably worse, more unstable training specifically in the first several dozen steps, exactly when the zero-initialization bias is largest, before it naturally fades away on its own regardless of whether it was corrected for or not.

## Explanation

`update_moments` computes both exponential moving averages directly: `beta1 * m + (1 - beta1) * grad` for `m`, `beta2 * v + (1 - beta2) * grad**2` for `v`.

`bias_correct` returns `moment / (1 - beta**t)`, the exact correction formula from Theory, used identically for both `m` and `v` with their respective `beta`.
