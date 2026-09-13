---
name: linear-regression-ridge-gradient
title: 'Stretch: L2 Regularization (Ridge)'
tags: [classical-ml, linear-regression, regularization, stretch]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Ordinary MSE only rewards matching the observed data. When features carry nearly the same information, many large, fragile weight combinations can fit equally well. Ridge regularization makes such solutions less attractive by charging for weight magnitude. It extends the gradient from `03-mse-gradient` without changing the model or the bias convention.

### From theory to code

Implement `ridge_grad` by asking `mse_gradient` for the data-fit gradient, then add the regularizer's contribution to the weight part only. Theory derives why the bias follows the original result unchanged.

### Constraints

- `input`, `weight`, `bias`, and `target` use the same shapes accepted by `mse_gradient`.
- Return a weight gradient with the same shape as `weight`.
- Return the exact base bias gradient, including `None` when `bias is None`.
- `lam=0` must match the unregularized MSE gradient.
- Penalize weights only; never add a penalty to the bias gradient.
- Reuse `mse_gradient` and do not mutate its returned arrays in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Treat regularization as an additional objective term, not a replacement for the MSE calculation.

</details>

<details>
<summary>Hint 2</summary>

The derivative of the squared-weight penalty has the same shape as `weight`, so it can be added directly to `grad_weight`.

</details>

## Theory

### The simple version

Ridge is a leash on the knobs of a model. Data can still pull each knob toward a better fit, but a far-from-zero knob feels a stronger pull back. The intercept is left alone because it represents the baseline rather than a feature's influence.

### The formula

The code corresponds to this objective and derivatives:

```text
L = MSE + lam * sum(weight ** 2)
grad_weight = grad_weight_mse + 2 * lam * weight
grad_bias = grad_bias_mse
```

The second line is vectorized over every element of `weight`; it remains valid when `grad_bias_mse` is `None`.

### How PyTorch actually implements this

Context only, untested by your submission: PyTorch optimizers such as `torch.optim.SGD` expose `weight_decay` for L2-style regularization. This exercise implements the equivalent gradient addition explicitly and deliberately excludes the bias.

## Explanation

`grad_weight, grad_bias = mse_gradient(input, weight, bias, target)` keeps the existing MSE behavior, including its handling of a missing bias. The return expression adds `2 * lam * weight` only to `grad_weight`; it creates a new result rather than altering the base gradient. `grad_bias` is returned as received, so a real bias is unpenalized and a `None` bias remains `None`.
