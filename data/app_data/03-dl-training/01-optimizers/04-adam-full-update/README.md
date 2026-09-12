---
name: dl-training-adam-full-update
title: 'Adam: full update rule'
tags: [optimization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`Adam: bias-corrected moment estimates` built the two pieces, `m` (a bias-corrected running average of the gradient, exactly `SGD + Momentum`'s velocity) and `v` (a bias-corrected running average of the SQUARED gradient, a new idea: tracking gradient MAGNITUDE separately from direction). This question assembles them into Adam's actual parameter update, and the way they combine is genuinely clever: `m_hat` decides WHICH WAY to step (momentum's own job), while `sqrt(v_hat)` decides HOW FAR, dividing the step down for any parameter whose gradients have consistently been large, and allowing a relatively bigger step for a parameter whose gradients have consistently been small.

This gives every parameter, effectively, its OWN adaptive learning rate, computed automatically from its own gradient history, rather than the single, uniform `lr` every parameter in `SGD`/`SGD + Momentum` shares.

### From theory to code

Theory updates and bias-corrects both moments (reusing `Adam: bias-corrected moment estimates`'s own functions directly), then combines them into one update: step opposite the corrected mean gradient, scaled by the learning rate and divided by the corrected root-mean-square gradient magnitude (plus a tiny `eps` for numerical safety).

Implement `adam_step(params, grads, m_list, v_list, t, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `t` starts at `1` (1-indexed), matching `bias_correct`'s own convention.
- Both `m_list` and `v_list` must be threaded through to the caller's next step (same pattern `SGD + Momentum`'s `velocities` used).
- `lr` defaults to `0.001`, matching real Adam's own much-smaller-than-SGD default (the adaptive per-parameter scaling means a smaller base `lr` is typically appropriate).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

For each `(param, grad, m, v)`, call `update_moments` then `bias_correct` on both results, exactly the two functions `Adam: bias-corrected moment estimates` already built.

</details>

<details>
<summary>Hint 2</summary>

The final update is `param - lr * m_hat / (np.sqrt(v_hat) + eps)`, one line, reusing the corrected moments you just computed.

</details>

## Theory

### The simple version

Two employees both get the same size raise, regardless of how CONSISTENTLY their performance has varied. A smarter system would give a smaller, steadier increase to someone whose performance swings wildly (don't overreact to noise), and allow a proportionally LARGER increase to someone whose performance has been steadily, consistently improving (that trend is trustworthy, lean into it). Adam applies exactly this idea to gradient updates: a parameter whose gradient has been consistently LARGE in magnitude gets its step size shrunk (to avoid overreacting), while a parameter whose gradient has been consistently small gets a relatively larger, more confident step, both computed automatically from each parameter's own recent history.

### The formula

```text
m_new, v_new = update_moments(m, v, grad, beta1, beta2)
m_hat = bias_correct(m_new, beta1, t)
v_hat = bias_correct(v_new, beta2, t)

param_new = param - lr * m_hat / (sqrt(v_hat) + eps)
```

`m_hat` (the corrected mean gradient) determines the step's DIRECTION, exactly `SGD + Momentum`'s own role. `sqrt(v_hat)` (the corrected root-mean-square gradient magnitude) determines the step's SCALE, dividing it down when that parameter's gradients have historically been large (curbing overreaction to noise or steep regions of the loss surface), and allowing a relatively larger effective step when gradients have historically been small (moving confidently through flat regions). `eps` exists purely as a numerical safety net, preventing division by exactly zero on the rare occasion `v_hat` collapses fully to `0`.

This combination, momentum for direction, an adaptive per-parameter scale for magnitude, is precisely what makes Adam, in practice, converge reliably on a very wide range of problems with comparatively little learning-rate tuning, one of the biggest reasons it became deep learning's default optimizer choice for so long.

### How PyTorch actually implements this

`torch.optim.Adam` implements exactly this formula (this question's implementation matches it precisely, across multiple consecutive steps, verified directly against real PyTorch). `AdamW: decoupled weight decay` (the very next question in this track) fixes a subtle, real flaw in how plain Adam interacts with L2 regularization, `Muon` (later in this track) is one of several more recent optimizers designed to improve on specific weaknesses Adam still has, but the core "momentum for direction, adaptive per-parameter scale for magnitude" idea this question builds remains the foundation nearly every modern deep learning optimizer, Adam's own many descendants included, is still built on top of.

## Explanation

`adam_step` loops over every `(param, grad, m, v)` tuple, calls `update_moments` and `bias_correct` (both imported, from `Adam: bias-corrected moment estimates`) to get `m_hat` and `v_hat`, and computes `param - lr * m_hat / (np.sqrt(v_hat) + eps)`, exactly the combined formula from Theory, collecting the updated params, `m`s, and `v`s into three new lists.
