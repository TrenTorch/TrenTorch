---
name: linear-regression-gd-step
title: One Gradient-Descent Update
tags: [classical-ml, linear-regression, gradient-descent, optimization]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`03-mse-gradient` told you which direction the loss gets WORSE in. To make it better, you move the opposite way — that's the entirety of gradient descent, one arithmetic step repeated many times.

The only design decision is how big a step to take. Too small and training crawls; too large and you can overshoot the minimum entirely, or bounce around it forever without settling. That step size is the learning rate, and it's the one number a training loop has to pick.

### From theory to code

Theory gives the update as a single subtraction per parameter: current value minus (step size times gradient). Both `weight` and `bias` follow the identical rule — the only branch is what happens when there's no `bias` to begin with.

Implement `gd_step(weight, bias, grad_weight, grad_bias, lr)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- Move `weight` and `bias` one step in the direction that reduces loss, scaled by `lr`, using the update rule from Theory.
- Return new values — never mutate `weight`, `bias`, `grad_weight` or `grad_bias` in place.
- If `bias` is `None` (no bias parameter, matching `01-hypothesis-function` and `03-mse-gradient`), return `None` for `updated_bias` too — there is nothing to step.
- Works for `weight`/`grad_weight` of any matching shape (scalar, vector, or matrix) — the update rule itself has no shape-specific logic.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The update is one line per parameter: `new_value = value - lr * grad`. There's no loop, no reshaping — the same expression works whatever shape `weight` happens to be.

</details>

<details>
<summary>Hint 2</summary>

Return `weight - lr * grad_weight`, not `weight -= lr * grad_weight`. NumPy arrays are passed by reference, so the in-place version would silently mutate the caller's original array.

</details>

## Theory

### The simple version

You're standing on a hillside in fog and want to reach the bottom. You can feel which way is downhill right where you stand (the gradient, from `03-mse-gradient`) — so you take one step that direction. How far you step is the learning rate: too timid and you barely move; too bold and you might stride right past the bottom.

### The formula

```text
weight = weight - lr * grad_weight
bias   = bias   - lr * grad_bias
```

`lr` controls how large a step is taken:

- too small → learning is very slow;
- too large → training may overshoot or become unstable.

`weight`/`grad_weight` and `bias`/`grad_bias` are updated by the exact same rule regardless of shape — `weight - lr * grad_weight` doesn't care whether `weight` is a scalar, a vector, or a matrix. Only `bias`'s optionality needs an explicit branch: `None` has no gradient to step against, so it stays `None`.

So the complete idea built up so far in this track is:

```text
1. Make predictions        (01-hypothesis-function)
2. Calculate loss          (02-mse-loss)
3. Calculate gradients     (03-mse-gradient)
4. Update parameters       (this question)
```

### How PyTorch actually implements this

`torch.optim.SGD` (with no momentum or weight decay) does exactly this update — `p.data -= lr * p.grad` for every parameter `p` — inside its `.step()` method. Momentum, weight decay and adaptive optimizers like Adam all build on this same one-line update, just adding extra bookkeeping (a running velocity, a per-parameter learning-rate scale) on top of the same core subtraction.

## Explanation

Returns `weight - lr * grad_weight`, never `weight -= lr * grad_weight`. The in-place version mutates the caller's original array — NumPy arrays are passed by reference, so `-=` would silently corrupt anything else still holding that same `weight`, exactly what the "does not mutate in place" test is there to catch.

`updated_bias` is computed the same way only when `bias` is not `None`. There's no `grad_bias` to apply when there was never a `bias` parameter to begin with, and returning a fabricated zero-stepped bias would silently invent a parameter that doesn't exist.
