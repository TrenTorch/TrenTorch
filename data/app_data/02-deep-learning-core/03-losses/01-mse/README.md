---
name: dl-core-mse-loss
title: MSE
tags: [deep-learning, loss-functions, autograd]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Every activation earlier in this section has a backward pass that flows into _something_ — eventually, that something is a loss function, the single number a whole network is trained to minimize. Mean squared error is the default choice for regression: it turns a whole batch of (prediction, target) pairs into one scalar by penalizing the squared distance between each pair.

### From theory to code

Implement `mse_loss_forward(input, target, reduction="mean")` and `mse_loss_backward(input, target, reduction="mean", grad_output=1.0)`, mirroring `torch.nn.functional.mse_loss`'s three reduction modes: `"mean"` (default), `"sum"`, `"none"`.

### Constraints

- `input`, `target`: matching NumPy array shapes.
- `reduction="mean"`: returns a scalar, the average squared error.
- `reduction="sum"`: returns a scalar, the total squared error.
- `reduction="none"`: returns the full elementwise squared-error array, same shape as `input`.
- `mse_loss_backward` takes the same `input`/`target`/`reduction`, plus `grad_output` (the upstream gradient, `1.0` by default), and returns a same-shape gradient array regardless of `reduction`.
- No Python loops; no mutating `input` or `target`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The elementwise squared error is the same regardless of `reduction` — only the final reduction step (`.mean()`, `.sum()`, or nothing) differs.

</details>

<details>
<summary>Hint 2</summary>

Whatever division the forward pass applies for `"mean"` (dividing by `input.size`), the backward pass must apply that exact same division to its gradient — otherwise gradients would silently scale with batch size.

</details>

## Theory

### The simple version

Squaring the error, instead of taking the absolute value, does two things worth knowing: large errors get penalized disproportionately more than small ones (an error of `2` contributes `4`, not `2`, so the loss cares a lot about outliers), and the loss stays smooth and differentiable everywhere, including at zero error, unlike `|error|`'s sharp kink at `0`.

### The formula

```text
elementwise:  e_i = (input_i - target_i)^2
mean:         L = (1/n) * sum(e_i)
sum:          L = sum(e_i)
none:         L = e (no reduction, the elementwise array itself)
```

Differentiating gives:

```text
dL/d_input_i = 2 * (input_i - target_i)     for "sum" and "none"
             = 2 * (input_i - target_i) / n  for "mean"
```

The `1/n` factor for `"mean"` is exactly the reduction's own division showing up again in the derivative — the same chain-rule bookkeeping that appears whenever a loss averages over a batch: the forward pass divides by `n`, so the backward pass must divide by `n` too, or gradients would silently scale with batch size.

### How PyTorch actually implements this

`torch.nn.functional.mse_loss(input, target, reduction=...)` implements exactly these three modes, and its autograd-derived backward pass matches the formula above exactly — verified in this exercise's own `tests.py`, whose `test_backward_matches_known_oracle_values` bakes in values generated once, offline, from `torch.nn.functional.mse_loss` plus autograd.

## Explanation

`mse_loss_forward` computes the elementwise squared error and reduces it according to `reduction`, exactly the three formulas in Theory.

`mse_loss_backward` computes the unreduced gradient `2 * (input - target)`, divides by `input.size` only when `reduction == "mean"` (matching the forward pass's own division), and multiplies by `grad_output` (the upstream gradient, `1.0` by default since a loss is usually the end of the computation graph).
