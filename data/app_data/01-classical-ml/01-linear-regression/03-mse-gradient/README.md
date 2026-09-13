---
name: linear-regression-mse-gradient
title: Gradient of MSE with Respect to w and b
tags: [classical-ml, linear-regression, manual-calculus, gradients]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-hypothesis-function` computes a prediction. `02-mse-loss` scores how wrong that prediction is. Neither one tells you which direction to nudge `weight` and `bias` to make that score smaller — that's a separate question, and it's the one this exercise answers.

The score is a single number computed from every prediction at once, so "which direction" isn't one number either — it's one number per entry of `weight` and one per entry of `bias`, each telling you how much that specific parameter contributed to the current wrongness. That collection of per-parameter directions is the gradient, and it's the only thing a training loop actually needs to know before it can improve anything.

### From theory to code

Theory derives it in two matched pieces: how the loss changes with the prediction, then how that flows back through the linear forward pass to `weight` and `bias`. The first piece is a direct derivative of the squared-error formula. The second piece reuses the exact shape relationship `01-hypothesis-function` established, just run in the opposite direction.

Implement `mse_gradient(input, weight, bias, target)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `input`: shape `(batch_size, in_features)`.
- `weight`: shape `(out_features, in_features)`.
- `bias`: shape `(out_features,)`, or `None`.
- `target`: shape `(batch_size, out_features)`.
- Returns `(grad_weight, grad_bias)`: `grad_weight` always has `weight`'s shape; `grad_bias` has `bias`'s shape, or is exactly `None` when `bias` is `None` — never a zero array standing in for it.
- The mean reduction is over every element (`batch_size * out_features` total), the same convention `02-mse-loss` uses.
- No autograd library. These are the manual derivatives.
- `input`, `weight`, `bias` and `target` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Start from the prediction, not from `weight` directly. `d(loss)/d(weight)` is easiest to find by first finding `d(loss)/d(prediction)`, then asking how `prediction` itself depends on `weight`.

</details>

<details>
<summary>Hint 2</summary>

`prediction = input @ weight.T (+ bias)`. Differentiating the mean of squares gives `d(loss)/d(prediction) = (2/N) * (prediction - target)`, where `N` is the total element count — not the batch size alone.

</details>

<details>
<summary>Hint 3</summary>

`weight`'s gradient is a matrix product (`d(loss)/d(prediction).T @ input`) because `weight` interacts with every feature of `input`. `bias`'s gradient is a plain sum over the batch axis, because `bias` is added identically to every row and doesn't interact with anything else.

</details>

## Theory

### The simple version

If the loss is a hill and `weight`/`bias` are your coordinates on it, the gradient just points uphill. A training loop moves the opposite way, downhill, one step at a time. This question computes which way "uphill" is — nothing more.

### The formula

For mean-reduced MSE, `loss = (1/N) * sum((prediction - target)**2)` where `N = batch_size * out_features`:

```text
d(loss)/d(prediction) = (2/N) * (prediction - target)
d(loss)/d(weight)     = d(loss)/d(prediction).T @ input
d(loss)/d(bias)       = sum(d(loss)/d(prediction), axis=0)
```

`weight`'s gradient is a matrix product because `weight` interacts with `input`. `bias`'s gradient is a plain sum because `bias` is added identically to every row — it doesn't interact with anything else. If `bias` is `None`, there's no bias parameter to have a gradient at all, so the correct return value is `None`, not a zero array standing in for it — the same distinction `01-hypothesis-function` draws for the forward pass.

### How PyTorch actually implements this

This is exactly what `loss.backward()` computes automatically once autograd is introduced later in this curriculum: it walks the same chain rule shown above, mechanically, by recording every operation `linear` and `mse_loss` performed and replaying their derivatives in reverse — the manual version here and autograd's automatic version compute the identical numbers, autograd just never needs you to write the formula down.

## Explanation

`prediction = input @ weight.T` (plus `bias` if given) recomputes the forward pass, since the gradient has to be evaluated at the current parameter values, not some other point.

`grad_prediction = (2 / element_count) * (prediction - target)` is `d(loss)/d(prediction)`, derived directly from differentiating the mean of squares.

`grad_weight = grad_prediction.T @ input` and `grad_bias = grad_prediction.sum(axis=0)` push that back through the linear forward pass — the same shape rules `01-hypothesis-function` established for the forward direction, run in reverse.
