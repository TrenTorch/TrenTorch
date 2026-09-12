---
name: dl-core-mse-loss
title: MSE
tags: [deep-learning, loss-functions, autograd]
difficulty: Beginner
---

## Statement

Implement:

```python
def mse_loss_forward(input, target, reduction="mean"): ...
def mse_loss_backward(input, target, reduction="mean", grad_output=1.0) -> np.ndarray: ...
```

Mirrors `torch.nn.functional.mse_loss`, supporting all three of PyTorch's reduction modes: `"mean"` (default), `"sum"`, `"none"`.

## Theory

Mean squared error is the default loss for regression: it penalizes the squared distance between each prediction and its target.

```text
elementwise:  e_i = (input_i - target_i)^2
mean:         L = (1/n) * sum(e_i)
sum:          L = sum(e_i)
none:         L = e (no reduction, the elementwise array itself)
```

Squaring the error, instead of taking the absolute value, has two consequences worth knowing: large errors are penalized disproportionately more than small ones (an error of `2` contributes `4`, not `2`), and the loss is smooth and differentiable everywhere, including at zero error, unlike `|error|`'s kink at `0`.

Differentiating gives:

```text
dL/d_input_i = 2 * (input_i - target_i)     for "sum" and "none"
             = 2 * (input_i - target_i) / n  for "mean"
```

The `1/n` factor for `"mean"` is exactly the reduction's own division showing up again in the derivative, the same chain-rule bookkeeping that appears whenever a loss averages over a batch: the forward pass divides by `n`, so the backward pass must divide by `n` too, or gradients would silently scale with batch size.

## Explanation

`mse_loss_forward` computes the elementwise squared error and reduces it according to `reduction`, exactly the three formulas in Theory.

`mse_loss_backward` computes the unreduced gradient `2 * (input - target)`, divides by `input.size` only when `reduction == "mean"` (matching the forward pass's own division), and multiplies by `grad_output` (the upstream gradient, `1.0` by default since a loss is usually the end of the computation graph).
