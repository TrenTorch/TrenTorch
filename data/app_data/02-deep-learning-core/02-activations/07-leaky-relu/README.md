---
name: dl-core-leaky-relu
title: LeakyReLU fwd/bwd
tags: [deep-learning, activations, autograd]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`01-relu`'s backward pass returns exactly `0` for every `x <= 0`. That's fine for a single forward/backward pass, but consider what happens over many training steps: if a unit's input lands negative for every example it ever sees, its gradient is `0` on every one of those steps too, so nothing about its weights ever changes. The unit is permanently stuck, "dead" for the rest of training, no matter how much more data arrives. This is the well-known "dying ReLU" problem, and it's a direct consequence of ReLU's gradient having no way back once it hits zero.

LeakyReLU exists to give a negative-going unit an escape hatch: keep almost all of ReLU's behavior (positive inputs pass through unchanged, negative inputs shrink toward zero), but never let the gradient hit exactly zero on the negative side, so a unit that goes negative can still receive a small nudge and recover.

### From theory to code

Theory's fix is a single number, `negative_slope`, that replaces ReLU's flat `0` region with a shallow line through the origin. Implement `leaky_relu_forward(x, negative_slope)` as this piecewise scaling, and `leaky_relu_backward(grad_output, x, negative_slope)` as its piecewise derivative, following the same "compute the local slope, then chain-rule multiply by `grad_output`" shape `01-relu`'s backward already uses.

### Constraints

- `x`: any shape, elementwise operation.
- `negative_slope`: a scalar, defaults to `0.01`, must be threaded through to both forward and backward.
- At `x == 0`, treat it as the `x <= 0` branch: `leaky_relu_forward` returns `0`, `leaky_relu_backward` returns `negative_slope` (the same convention `01-relu` uses at its own kink, just with a different value on the negative side).
- One vectorized expression per function, no explicit loop over elements.
- Neither function modifies `x` or `grad_output` in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

This is `01-relu`'s piecewise `x > 0` test again, just with a different value plugged into the "otherwise" branch. `np.where` (or equivalent) is still the right tool.

</details>

<details>
<summary>Hint 2</summary>

The forward branch scales `x` itself (`negative_slope * x`) when `x <= 0`; the backward branch just returns the constant `negative_slope`, it isn't multiplied by `x` there, the slope of a line through the origin is the same everywhere on that line.

</details>

## Theory

### The simple version

Think of ReLU as a one-way valve: positive flow passes, negative flow is sealed off completely, no way back. LeakyReLU is the same valve with a pinhole drilled through the seal, negative flow still gets choked down to a trickle, but it's never fully sealed. That trickle is enough for gradient information to keep flowing backward through a unit that's currently outputting a negative value, instead of that unit going silent forever.

### The formula

```text
LeakyReLU(x) = x                     if x > 0
             = negative_slope * x    otherwise

d/dx LeakyReLU(x) = 1               if x > 0
                   = negative_slope  otherwise
```

with `negative_slope` typically a small constant like `0.01`. Negative inputs still shrink toward `0`, preserving ReLU's sparsity-inducing behavior, but they keep a small, nonzero gradient, so a unit that goes negative can still receive a (small) gradient signal and recover, rather than dying permanently.

### How PyTorch actually implements this

`torch.nn.functional.leaky_relu(x, negative_slope=0.01)` computes exactly this piecewise function and its gradient. `tests.py` bakes in reference values generated once, offline, from real `torch.nn.functional.leaky_relu` forward and backward passes.

## Explanation

`leaky_relu_forward` uses `np.where(x > 0.0, x, negative_slope * x)`, the piecewise definition from Theory, applied elementwise.

`leaky_relu_backward` uses `np.where(x > 0.0, 1.0, negative_slope)` for the local derivative, then returns `grad_output * local_grad`, the same "compute the local slope, then chain-rule multiply" shape `01-relu`'s backward uses, just with `negative_slope` in place of `0` on the negative branch.
