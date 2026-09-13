---
name: linear-regression-training-loop
title: Full Linear Regression Training Loop
tags: [classical-ml, linear-regression, training-loop]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-hypothesis-function`, `02-mse-loss`, `03-mse-gradient`, and `04-gd-step` each solve one part of fitting a line. A model becomes useful only when those parts run repeatedly: make predictions, measure their error, find which direction reduces it, and move the parameters. This question wires that full-batch loop together without losing the single-output shapes established earlier.

### From theory to code

Implement `train_linear_regression`. Initialize the parameters once, turn the one-dimensional targets into the one-column form expected by the earlier helpers, then use their gradient and update operations for each epoch.

### Constraints

- `input` has shape `(batch_size, in_features)` and `target` has shape `(batch_size,)`.
- Return `weight` with shape `(1, in_features)` and `bias` with shape `(1,)`.
- Start both returned parameters at zero before any updates.
- Reshape `target` once to `(batch_size, 1)` before computing gradients.
- Run exactly `epochs` full-batch gradient-descent steps; `epochs=0` returns the zero initialization.
- Reuse `mse_gradient` and `gd_step`; do not reimplement either calculation.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The output of a single-output `linear` call is a column, even when the caller supplies targets as a flat array.

</details>

<details>
<summary>Hint 2</summary>

Create the zero `weight` from `input.shape[1]`, create `bias` with one element, and reshape `target` before the loop.

</details>

<details>
<summary>Hint 3</summary>

Each loop iteration is just `grad_weight, grad_bias = mse_gradient(...)` followed by `weight, bias = gd_step(...)` using the same `lr`.

</details>

## Theory

### The simple version

Fitting is repeated course correction. Start with a deliberately uninformative estimate, ask how every parameter contributed to the current misses, make a small correction, and repeat. Full-batch training asks that question using every example before each correction.

### The formula

With `W_0 = 0` and `b_0 = 0`, one epoch uses the earlier MSE gradient and update:

```text
(dW_t, db_t) = mse_gradient(X, W_t, b_t, y.reshape(-1, 1))
(W_{t+1}, b_{t+1}) = gd_step(W_t, b_t, dW_t, db_t, lr)
```

Repeat this exactly `epochs` times. The reshape is part of the computation's shape contract: predictions and targets are both `(batch_size, 1)`.

### How PyTorch actually implements this

Context only, untested by your submission: the test suite includes an offline-generated reference for a zero-initialized `torch.nn.Linear(2, 1)` trained with `torch.nn.MSELoss` and `torch.optim.SGD` for 50 full-batch steps. In normal PyTorch code, `loss.backward()` supplies the gradients and `optimizer.step()` performs the update.

## Explanation

`weight = np.zeros((1, input.shape[1]))` preserves the row-vector convention used by `linear`, while `bias = np.zeros(1)` supplies its one output bias. `target_2d = target.reshape(-1, 1)` occurs outside the loop, so every `mse_gradient` call receives the matching column shape rather than relying on accidental broadcasting. The `for _ in range(epochs)` body delegates the calculation to `mse_gradient` and immediately delegates the parameter change to `gd_step`; with zero epochs, that body never runs and the initialization is returned unchanged.
