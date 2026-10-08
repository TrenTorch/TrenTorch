---
name: research-adam-minimize
title: 'Adam: Running the Full Optimization Loop'
tags: [research-papers, optimization, adam]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`02-adam-single-step` computes one Adam update. Training repeats that update many times, and the moments must carry over from one step to the next. This question wraps the single step in the loop that training actually runs, then uses it to minimize a simple function you can check by eye: `f(x) = x²`, whose gradient is `2x` and whose minimum is at `0`.

### From theory to code

Implement `adam_minimize(grad_fn, theta0, steps, lr, beta1, beta2, eps)`. It runs `steps` Adam updates starting from `theta0` and returns the full trajectory: the starting value followed by the value after each update. The signature and docstring are already in the editor.

### Constraints

- The trajectory has length `steps + 1`.
- `grad_fn` takes the current `theta` and returns the gradient at that point.
- Works on scalars and NumPy arrays.

### Hints

<details>
<summary>Hint 1</summary>

Keep `m` and `v` as variables outside the loop, initialized to zeros the same shape as `theta`. Update them every iteration.

</details>

<details>
<summary>Hint 2</summary>

Inside the loop, the step counter `t` starts at 1, not 0, because bias correction divides by `1 - beta**t`.

</details>

## Theory

### The simple version

Picture a ball rolling downhill. Each step you check the slope (the gradient), update your memory of the recent slopes (`m` and `v`), and take a step whose size is set by how consistent those slopes have been. The loop repeats until the ball settles. Adam's trick is that the step length is controlled per parameter, not by the raw slope.

### The formula

$$
\theta_t = \theta_{t-1} - \alpha \, \frac{\hat m_t}{\sqrt{\hat v_t} + \epsilon}, \qquad t = 1, 2, \ldots, T
$$

- `\theta_t` — the parameter after `t` updates.
- `T` — the number of updates, `steps` in code.
- Each `\hat m_t, \hat v_t` is computed from the gradients seen so far, as in `02-adam-single-step`.

### Sanity check on `f(x) = x²`

From `x=1` with `lr=0.1`, the first update moves to `0.9`, the second to about `0.8004`, and the value keeps shrinking toward `0`. The step size stays close to `lr` while the gradient keeps the same sign, which is why Adam makes steady progress on this kind of function.

### How NumPy/PyTorch actually implements this

`torch.optim.Adam(params, lr=...)` wraps this loop: `loss.backward()` supplies the gradients, and `optimizer.step()` runs one update per parameter, keeping `exp_avg` and `exp_avg_sq` as state. Calling `step()` in a loop, as this question does by hand, is what a training script does.

## Explanation

`adam_minimize` starts from `theta0`, then for each `t` from 1 to `steps` it calls `grad_fn`, updates `m` and `v`, bias-corrects them, and applies the update. A copy of `theta` is appended to the trajectory after each step so the caller sees every intermediate value. Copying matters: without it, every entry would point to the same array and the list would show only the final value.
