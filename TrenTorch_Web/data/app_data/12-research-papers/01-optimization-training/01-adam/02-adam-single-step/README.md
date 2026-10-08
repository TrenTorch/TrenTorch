---
name: research-adam-single-step
title: 'Adam: One Full Update With Bias Correction'
tags: [research-papers, optimization, adam]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-adam-moment-updates` built the two running averages. A full Adam step still needs two more things. First, the averages start at zero, so early steps underestimate them; Adam corrects for this. Second, the step itself is the bias-corrected first moment divided by the square root of the bias-corrected second moment. Together these produce a step size that adapts to each parameter.

### From theory to code

Implement `adam_step(theta, grad, m, v, t, lr, beta1, beta2, eps)`. It updates the moments, bias-corrects them, applies the update, and returns `(theta, m, v)`. The signature and docstring are already in the editor.

### Constraints

- `t` is 1-based: the first call uses `t=1`.
- Defaults are the paper's: `lr=0.001`, `beta1=0.9`, `beta2=0.999`, `eps=1e-8`.
- Works on scalars and NumPy arrays.

### Hints

<details>
<summary>Hint 1</summary>

Reuse the moment update from the previous question, then divide each moment by `1 - beta**t` before using it.

</details>

<details>
<summary>Hint 2</summary>

The parameter moves by `lr * m_hat / (sqrt(v_hat) + eps)`. Subtract that from `theta`; the minus sign points the step against the gradient.

</details>

## Theory

### The simple version

At the very first step, both averages are only 10% and 0.1% of their true size, because they started from zero. Dividing by `1 - beta**t` scales them back up. Once `t` is large those factors approach 1 and the correction disappears. The step is then roughly `lr` in size, whatever the gradient's scale, because the first moment is divided by the square root of the second.

### The formula

$$
\hat m_t = \frac{m_t}{1 - \beta_1^t} \qquad \hat v_t = \frac{v_t}{1 - \beta_2^t}
$$

$$
\theta_t = \theta_{t-1} - \alpha \, \frac{\hat m_t}{\sqrt{\hat v_t} + \epsilon}
$$

- `\hat m_t, \hat v_t` — bias-corrected moments.
- `\alpha` — the learning rate, `lr` in code.
- `\epsilon` — a small constant (e.g. `1e-8`) that prevents division by zero.

### Why the step is about `lr` in size

For a single parameter whose gradient is steady, `\hat m_t \approx g` and `\sqrt{\hat v_t} \approx |g|`, so the ratio is about `±1`. The update is therefore about `±\alpha` regardless of how large `g` is. That is the scale invariance the paper emphasizes.

### How NumPy/PyTorch actually implements this

`torch.optim.Adam` does this in place, per parameter, with `bias_correction1` and `bias_correction2` computed from `step`. Its update line is `param.addcdiv_(exp_avg, denom, value=-step_size)`, where `denom = sqrt(exp_avg_sq)/sqrt(bias_correction2) + eps`. That is the same arithmetic written out in this question.

## Explanation

`adam_step` first updates `m` and `v` with the same formulas as before. It then divides each by its bias-correction term, `1 - beta**t`. The parameter update divides the corrected first moment by the square root of the corrected second moment, plus `eps`, and scales by `lr`. The function returns the new `theta` and the new moments so the caller can carry state forward.
