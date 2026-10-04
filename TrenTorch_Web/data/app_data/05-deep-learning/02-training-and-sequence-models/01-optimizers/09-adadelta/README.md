---
name: dl-training-adadelta
title: Adadelta
tags: [deep-learning, optimization, training]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Adagrad adapts the learning rate for each parameter by accumulating squared gradients. This works well when parameters have different update frequencies, but its accumulator only grows over time.

As the accumulated squared gradients become larger, the effective learning rate keeps getting smaller. Eventually, updates can become extremely small even when further learning would still be useful.

Adadelta addresses this by replacing the ever-growing sum with exponentially decaying averages. It keeps track of two quantities:

1. A moving average of squared gradients.
2. A moving average of squared parameter updates.

The update used in this exercise is:

$$
\text{square\_avg}_{\text{new}}
=
\rho \cdot \text{square\_avg}
+
(1-\rho)\cdot\text{grad}^2
$$

$$
\text{delta}
=
\frac{
\sqrt{\text{acc\_delta}+\text{eps}}
}{
\sqrt{\text{square\_avg}_{\text{new}}+\text{eps}}
}
\cdot
\text{grad}
$$

$$
\text{param}_{\text{new}}
=
\text{param}
-
\text{lr}\cdot\text{delta}
$$

$$
\text{acc\_delta}_{\text{new}}
=
\rho\cdot\text{acc\_delta}
+
(1-\rho)\cdot\text{delta}^2
$$

Both `square_avg` and `acc_delta` start at zeros.

### From theory to code

Implement:

```python
adadelta_step(
    param,
    grad,
    square_avg,
    acc_delta,
    lr,
    rho,
    eps,
)
```

The function returns:

```python
(new_param, new_square_avg, new_acc_delta)
```

The signature is provided in the editor.

The function should first update the moving average of squared gradients. That value determines the scale of the current update.

After computing the update `delta`, use it to update both the parameter and the moving average of squared updates.

### Constraints

- `param`, `grad`, `square_avg`, and `acc_delta` must have the same shape. A mismatch raises `ValueError`.
- `lr` must be greater than `0`. Otherwise, raise `ValueError`.
- `rho` must be in `[0, 1)`. Otherwise, raise `ValueError`.
- `eps` must be greater than `0`. Otherwise, raise `ValueError`.
- Inputs must not be modified.
- Return new arrays.
- `square_avg` starts at zeros.
- `acc_delta` starts at zeros.

### Hints

<details>
<summary>Hint 1</summary>

Compute `square_avg_new` first. It is an exponentially weighted average of the squared gradient.

</details>

<details>
<summary>Hint 2</summary>

Compute `delta` using both the previous `acc_delta` and the newly computed `square_avg_new`.

</details>

<details>
<summary>Hint 3</summary>

After computing `delta`, use it to update both `param` and `acc_delta`.

</details>

## Theory

### The simple version

Imagine adjusting the size of your steps based on two kinds of history.

First, you remember how large the gradients have recently been. Large recent gradients suggest that future steps should be scaled down.

Second, you remember how large your previous parameter updates have been. If recent updates were large, the algorithm can use that history to determine an appropriate scale for the next update.

Unlike Adagrad, this history does not grow forever. Older observations gradually lose their influence because the averages use the decay factor `rho`.

The result is an adaptive optimizer that bases the current update on recent gradient and update magnitudes.

### The formula

First update the exponential moving average of squared gradients:

$$
\text{square\_avg}_{\text{new}}
=
\rho \cdot \text{square\_avg}
+
(1-\rho)\cdot\text{grad}^2
$$

Then calculate the parameter update:

$$
\text{delta}
=
\frac{
\sqrt{\text{acc\_delta}+\text{eps}}
}{
\sqrt{\text{square\_avg}_{\text{new}}+\text{eps}}
}
\cdot
\text{grad}
$$

Then update the parameter:

$$
\text{param}_{\text{new}}
=
\text{param}
-
\text{lr}\cdot\text{delta}
$$

Finally, update the moving average of squared updates:

$$
\text{acc\_delta}_{\text{new}}
=
\rho\cdot\text{acc\_delta}
+
(1-\rho)\cdot\text{delta}^2
$$

The symbols mean:

- $\text{param}$ is the current parameter.
- $\text{grad}$ is the current gradient.
- $\text{square\_avg}$ stores the moving average of squared gradients.
- $\text{square\_avg}_{\text{new}}$ is the updated squared-gradient average.
- $\text{acc\_delta}$ stores the moving average of squared parameter updates.
- $\text{acc\_delta}_{\text{new}}$ is the updated squared-update average.
- $\rho$ controls how quickly old observations decay.
- $\text{eps}$ provides numerical stability.
- $\text{delta}$ is the scaled parameter update.
- $\text{lr}$ is the learning rate.
- $\text{param}_{\text{new}}$ is the updated parameter.

The ratio

$$
\frac{
\sqrt{\text{acc\_delta}+\text{eps}}
}{
\sqrt{\text{square\_avg}_{\text{new}}+\text{eps}}
}
$$

adapts the scale of the current gradient using recent update history and recent gradient history.

### Where it fits

Adadelta is an adaptive optimization method related to Adagrad.

The key difference is that Adagrad keeps an ever-growing sum of squared gradients, while Adadelta uses exponentially decaying averages.

In PyTorch, the corresponding optimizer is:

```python
torch.optim.Adadelta(
    parameters,
    lr=learning_rate,
    rho=rho,
    eps=epsilon,
)
```

Adadelta is therefore part of the adaptive optimizer family alongside methods such as Adagrad and Adam.

### How PyTorch actually implements this

PyTorch provides Adadelta through `torch.optim.Adadelta`.

The optimizer maintains state corresponding to the squared-gradient moving average and the squared-update moving average. Each optimization step updates those states and uses them to scale the parameter update.

A production implementation also handles parameter groups, device placement, data types, optional weight decay, sparse parameters, optimizer state initialization, and other framework-level details.

This exercise focuses only on the core update and is not intended to reproduce the complete PyTorch optimizer implementation.

### Production connections

Adadelta can be useful when an adaptive optimizer is desired without relying on a permanently growing gradient accumulator.

A configuration might look like:

```yaml
optimizer: adadelta
learning_rate: 1.0
rho: 0.9
eps: 1.0e-6
```

The exact values depend on the model, gradient scale, dataset, and training recipe.

Unlike Adagrad, Adadelta was designed to reduce dependence on manually selecting a global learning rate, although the learning rate remains an explicit parameter in the implementation used here.

### Decision-making

Pick Adadelta when:

- You want an adaptive optimizer based on recent gradient history.
- You want exponentially decaying state instead of Adagrad's continually growing accumulator.
- A training recipe has been validated with Adadelta.
- You want to experiment with an optimizer that tracks both gradient magnitude and update magnitude.

Adagrad can be preferable when sparse feature updates are particularly important and its shrinking learning rate is acceptable.

SGD with momentum can be preferable when a simpler optimizer with a well-tuned learning rate schedule is sufficient.

Adam-style optimizers are often preferred for modern deep learning workloads because they provide adaptive scaling together with first-moment and second-moment state.

### Pros and cons

#### Pros

- Uses exponentially decaying averages instead of an ever-growing accumulator.
- Adapts the update scale using recent gradient and update history.
- Maintains a fixed amount of optimizer state per parameter.
- Can be less sensitive to the long-term accumulation problem of Adagrad.

#### Cons

- Requires maintaining two parameter-sized state arrays.
- Introduces interactions between `lr`, `rho`, and `eps`.
- May not outperform Adam on many modern deep learning workloads.
- The update rule is more involved than SGD or momentum.

## Explanation

The solution follows the mathematical update in four stages.

First, update the moving average of squared gradients:

```python
square_avg_new = (
    rho * square_avg
    + (1 - rho) * grad * grad
)
```

This state represents recent gradient magnitude.

Next, calculate the scaled update:

```python
delta = (
    np.sqrt(acc_delta + eps)
    / np.sqrt(square_avg_new + eps)
    * grad
)
```

The numerator uses the history of previous update magnitudes, while the denominator uses the newly updated gradient history.

Then update the parameter:

```python
param_new = param - lr * delta
```

Finally, record the magnitude of the current update:

```python
acc_delta_new = (
    rho * acc_delta
    + (1 - rho) * delta * delta
)
```

The order matters. `square_avg_new` must be used when computing `delta`, and `delta` must be used when updating `acc_delta_new`.

The implementation does not modify any input arrays. NumPy expressions create the returned arrays while preserving the original parameter, gradient, and optimizer state.
