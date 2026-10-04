---
name: dl-training-nesterov-momentum
title: Nesterov Momentum
tags: [deep-learning, optimization, training]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Plain momentum can overshoot in narrow valleys because its velocity keeps pushing the parameters forward even after the gradient has turned around.

This is the problem addressed by [SGD with momentum](../02-sgd-momentum/). Nesterov momentum lets the gradient look one step ahead before committing to the parameter update.

In this exercise, use this reparameterized form of Nesterov's method:

$$
v_{\text{new}} = \text{momentum} \cdot v + \text{grad}
$$

$$
\text{param}_{\text{new}}
=
\text{param}
-
\text{lr}
\left(
\text{grad}
+
\text{momentum} \cdot v_{\text{new}}
\right)
$$

The gradient is evaluated at the current parameter. Initial velocity is zeros.

This is a reparameterized form of Nesterov's method. It matches the textbook update up to a change of variables, which is how PyTorch's `SGD(nesterov=True)` is written.

### From theory to code

Implement:

```python
nesterov_step(param, grad, velocity, lr, momentum)
```

The function returns:

```python
(new_param, new_velocity)
```

The signature is provided in the editor.

### Constraints

- `param`, `grad`, and `velocity` must have the same shape. A mismatch raises `ValueError`.
- `momentum` must be in `[0, 1)`. Otherwise, raise `ValueError`.
- Inputs must not be modified.
- Return new arrays.
- With `momentum = 0`, the result must equal plain SGD.

### Hints

<details>
<summary>Hint 1</summary>

Compute the new velocity first.

</details>

<details>
<summary>Hint 2</summary>

The parameter update uses the new velocity, not the old velocity.

</details>

<details>
<summary>Hint 3</summary>

Write both update lines and compare them with the momentum version.

</details>

## Theory

### The simple version

Imagine skiing down a narrow valley.

Classical momentum keeps going in the direction its velocity is already carrying it. When the valley turns, that velocity can keep pushing the skier in the wrong direction.

Nesterov momentum asks how the current gradient should change the direction where momentum is about to carry you. It therefore accounts for the momentum contribution before committing to the next parameter position.

### The formula

First compute the new velocity:

$$
v_{\text{new}}
=
\text{momentum} \cdot v
+
\text{grad}
$$

Then update the parameter:

$$
\text{param}_{\text{new}}
=
\text{param}
-
\text{lr}
\left(
\text{grad}
+
\text{momentum} \cdot v_{\text{new}}
\right)
$$

Here:

- $\text{param}$ is the current parameter.
- $\text{grad}$ is the gradient evaluated at the current parameter.
- $v$ is the current velocity.
- $v_{\text{new}}$ is the updated velocity.
- $\text{momentum}$ controls how much previous velocity is retained.
- $\text{lr}$ is the learning rate.
- $\text{param}_{\text{new}}$ is the updated parameter.

Classical momentum instead uses:

$$
v_{\text{new}}
=
\text{momentum} \cdot v
+
\text{grad}
$$

followed by:

$$
\text{param}_{\text{new}}
=
\text{param}
-
\text{lr} \cdot v_{\text{new}}
$$

Nesterov uses the current gradient together with the momentum contribution from the new velocity.

### Where it fits

Nesterov momentum is a variant of SGD with momentum. In PyTorch, it is exposed through:

```python
torch.optim.SGD(
    parameters,
    lr=learning_rate,
    momentum=momentum,
    nesterov=True,
)
```

### How PyTorch actually implements this

PyTorch's `torch.optim.SGD` supports Nesterov momentum through `nesterov=True`.

Conceptually, the optimizer maintains a momentum buffer and combines the current gradient with the momentum contribution when computing the parameter update.

The implementation in this exercise focuses only on the core update rule. A production optimizer also handles concerns such as parameter groups, weight decay, dampening, sparse gradients, maximization, and optimizer state management.

This section is context only and is not tested.

### Production connections

SGD with momentum and Nesterov momentum appear in training recipes for vision models and other workloads where SGD has been tuned successfully.

A configuration might look like:

```yaml
optimizer: sgd
learning_rate: 0.01
momentum: 0.9
nesterov: true
```

The appropriate values depend on the model, dataset, batch size, learning rate schedule, and the rest of the training recipe.

### Decision-making

Pick Nesterov momentum when you are already using SGD with momentum, the optimization problem is relatively smooth, and a validated training recipe benefits from it.

Plain momentum can be preferable when simplicity matters or experiments show no measurable gain from Nesterov momentum.

Adam-style optimizers can make this choice less important in many deep learning workloads because they combine momentum-like behavior with adaptive parameter-wise scaling.

### Pros and cons

#### Pros

- Often converges faster on smooth optimization problems.
- Uses the same velocity-sized state as classical momentum.

#### Cons

- Introduces another interaction between the learning rate and momentum.
- Can provide little gain on noisy deep network training.
- Adam often performs better on many deep network workloads.

## Explanation

A textbook presentation of Nesterov momentum often describes evaluating the gradient at a look-ahead point. That formulation is useful for understanding the intuition, but it would require the caller to evaluate the gradient at a shifted parameter.

The implementation here instead keeps the gradient evaluation at the current parameter:

$$
v_{\text{new}}
=
\text{momentum} \cdot v
+
\text{grad}
$$

followed by:

$$
\text{param}_{\text{new}}
=
\text{param}
-
\text{lr}
\left(
\text{grad}
+
\text{momentum} \cdot v_{\text{new}}
\right)
$$

The two forms match up to a change of variables.

This means the caller can use a standard gradient function:

```python
grad = gradient(param)

new_param, new_velocity = nesterov_step(
    param,
    grad,
    velocity,
    lr,
    momentum,
)
```

The caller does not need to explicitly construct a look-ahead parameter or evaluate a gradient at that shifted point.
