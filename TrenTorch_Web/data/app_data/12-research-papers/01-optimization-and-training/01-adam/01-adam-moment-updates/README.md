---
name: research-adam-moment-updates
title: 'Adam: Updating the Two Running Moments'
tags: [research-papers, optimization, adam]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Plain gradient descent uses one global learning rate for every parameter. Adam (Kingma & Ba, 2014) keeps two running averages per parameter instead: one of the gradients themselves (the direction to move) and one of the squared gradients (how big the steps have been, so each parameter can get its own effective step size). This question implements only the bookkeeping that keeps those two averages up to date, which is the first thing Adam does on every training step.

### From theory to code

Implement `adam_update_moments(m, v, grad, beta1, beta2)`. It takes the previous first and second moment and the current gradient, and returns the two new moments. The signature and docstring are already in the editor.

### Constraints

- `m` and `v` start at zero for a fresh parameter.
- `beta1` and `beta2` default to the paper's values, `0.9` and `0.999`.
- Works on scalars and NumPy arrays of the same shape.

### Hints

<details>
<summary>Hint 1</summary>

Each moment is a weighted blend of its old value and a new quantity. The first moment blends the old `m` with `grad`; the second blends the old `v` with `grad**2`.

</details>

<details>
<summary>Hint 2</summary>

Use `beta` as the weight on the old value and `1 - beta` as the weight on the new one. That's what keeps each average stable, instead of growing with the number of steps.

</details>

## Theory

### The simple version

Imagine tracking how fast you've been walking. The first moment is your average velocity over recent steps (signed, so going backward cancels going forward). The second moment is your average squared speed (always positive, so it measures how large the moves have been regardless of direction). Adam uses the first to pick a direction and the second to scale the step. This question only builds the two running averages.

### The formula

$$
m_t = \beta_1 m_{t-1} + (1 - \beta_1)\, g_t \qquad v_t = \beta_2 v_{t-1} + (1 - \beta_2)\, g_t^2
$$

- `m_t` — first moment at step `t`, an exponential moving average of gradients.
- `v_t` — second moment at step `t`, an exponential moving average of squared gradients.
- `g_t` — the gradient at step `t`.
- `\beta_1, \beta2` — decay rates; each close to 1 so old values fade slowly.

### Why the averages start too small

Both moments start at zero, so for the first few steps they are biased toward zero. The paper corrects this later with `1 - \beta^t` factors. That correction is part of `02-adam-single-step`, not this question.

### How NumPy/PyTorch actually implements this

`torch.optim.Adam` keeps `exp_avg` (this `m`) and `exp_avg_sq` (this `v`) as one tensor per parameter and updates them in place with `lerp_` and `mul_`/`addcmul_`, exactly these two lines. The same bookkeeping, done element-wise on arrays, is what this question asks for.

## Explanation

`adam_update_moments` computes `beta1 * m + (1 - beta1) * grad` and `beta2 * v + (1 - beta2) * grad**2`. Both operations are element-wise, so the same code works for a scalar or for a whole parameter array. The function returns new values rather than mutating `m` and `v`, which keeps the caller in control of state.
