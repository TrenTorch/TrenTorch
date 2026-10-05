---
name: dl-training-adagrad
title: Adagrad
tags: [deep-learning, optimization, training]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A single learning rate does not always work equally well for every parameter.

Some parameters may receive large gradients over and over again, while others may receive small or infrequent gradients. Applying the same step size to every parameter can make frequently updated parameters move too aggressively and make sparse parameters learn too slowly.

Adagrad addresses this by keeping a running sum of squared gradients for every parameter. Parameters that have accumulated larger squared gradients receive smaller future updates.

The update used in this exercise is:

$$
\text{accum}_{\text{new}}
=
\text{accum}
+
\text{grad}^2
$$

$$
\text{param}_{\text{new}}
=
\text{param}
-
\text{lr}
\frac{\text{grad}}
{\sqrt{\text{accum}_{\text{new}}} + \text{eps}}
$$

The accumulator starts at zeros.

### From theory to code

Implement:

```python
adagrad_step(param, grad, accum, lr, eps)
```

The function returns:

```python
(new_param, new_accum)
```

The signature is provided in the editor.

The accumulator stores the element-wise sum of squared gradients seen so far. It is updated before calculating the parameter update.

### Constraints

- `param`, `grad`, and `accum` must have the same shape. A mismatch raises `ValueError`.
- `lr` must be greater than `0`. Otherwise, raise `ValueError`.
- `eps` must be greater than `0`. Otherwise, raise `ValueError`.
- Inputs must not be modified.
- Return new arrays.
- The accumulator starts at zeros.
- The squared gradient and accumulator are element-wise operations.

### Hints

<details>
<summary>Hint 1</summary>

Compute the new accumulator before computing the parameter update.

</details>

<details>
<summary>Hint 2</summary>

The denominator uses the square root of the new accumulator plus `eps`.

</details>

<details>
<summary>Hint 3</summary>

Write the two update lines exactly as given, then translate each operation directly into NumPy.

</details>

## Theory

### The simple version

Imagine giving every student a personal difficulty score based on how much practice they have already received.

If a parameter has received large gradients many times, its accumulated score becomes large. Adagrad then reduces the size of future updates for that parameter.

If another parameter has received only small or occasional gradients, its accumulated value stays smaller, so it can continue taking relatively larger steps.

The important idea is that the learning rate becomes parameter-specific.

### The formula

First accumulate the squared gradient:

$$
\text{accum}_{\text{new}}
=
\text{accum}
+
\text{grad}^2
$$

Then update the parameter:

$$
\text{param}_{\text{new}}
=
\text{param}
-
\text{lr}
\frac{\text{grad}}
{\sqrt{\text{accum}_{\text{new}}} + \text{eps}}
$$

Here:

- $\text{param}$ is the current parameter.
- $\text{grad}$ is the current gradient.
- $\text{accum}$ is the accumulated squared-gradient state.
- $\text{accum}_{\text{new}}$ is the updated accumulator.
- $\text{lr}$ is the base learning rate.
- $\text{eps}$ is a small positive value that prevents numerical problems when the denominator is very small.
- $\text{param}_{\text{new}}$ is the updated parameter.

The accumulator is maintained independently for every parameter element.

For example, if one parameter repeatedly receives a large gradient, its accumulator grows quickly:

$$
\text{accum}
=
g_1^2 + g_2^2 + \cdots + g_t^2
$$

The effective learning rate for that parameter therefore decreases as more gradient information accumulates.

### Where it fits

Adagrad is an adaptive optimization algorithm. Unlike plain SGD, it does not use exactly the same effective learning rate for every parameter.

It is especially associated with problems containing sparse features or parameters that are updated at very different frequencies.

A typical optimizer configuration conceptually looks like:

```python
torch.optim.Adagrad(
    parameters,
    lr=learning_rate,
    eps=epsilon,
)
```

### How PyTorch actually implements this

PyTorch provides Adagrad through `torch.optim.Adagrad`.

The optimizer maintains an accumulated squared-gradient state for each parameter and uses that state to scale subsequent updates.

A production implementation also has to manage optimizer state, parameter groups, device placement, data types, optional weight decay, sparse gradients, and other framework-level concerns.

The implementation in this exercise focuses only on the core Adagrad update and is not intended to reproduce the complete optimizer implementation.

### Production connections

Adagrad is useful when different parameters can have very different gradient frequencies.

A common historical application is sparse or high-dimensional feature learning, where some features occur frequently while others occur rarely.

A configuration might look like:

```yaml
optimizer: adagrad
learning_rate: 0.01
eps: 1.0e-10
```

The appropriate learning rate and numerical stability constant depend on the model, gradient scale, data representation, and training setup.

### Decision-making

Pick Adagrad when:

- Parameters have very different update frequencies.
- Sparse gradients are important.
- Per-parameter learning-rate adaptation is useful.
- You want a simple adaptive method without maintaining momentum and second-moment states separately.

Plain SGD can be preferable when a well-tuned fixed learning rate is sufficient.

Momentum-based SGD can be preferable when preserving a directional velocity is more useful than continually shrinking the effective learning rate.

Adam-style optimizers are often preferred for modern deep networks because they combine first-moment and second-moment adaptation and do not continually shrink the effective learning rate in the same way as Adagrad.

### Pros and cons

#### Pros

- Automatically adapts the learning rate for each parameter.
- Can work well with sparse and infrequent features.
- Requires only one additional parameter-sized accumulator.
- Does not require manually choosing a separate learning rate for every parameter.

#### Cons

- The accumulated squared gradients continually grow.
- The effective learning rate can become very small after long training.
- It can be less effective than Adam or other modern adaptive optimizers on many deep learning workloads.
- The learning rate still requires tuning.

## Explanation

The key part of Adagrad is the accumulated squared-gradient state.

The accumulator must be updated first:

$$
\text{accum}_{\text{new}}
=
\text{accum}
+
\text{grad}^2
$$

The new accumulator is then used in the denominator:

$$
\sqrt{\text{accum}_{\text{new}}} + \text{eps}
$$

This ordering matters because the current gradient should immediately contribute to the scaling of the current update.

The implementation therefore follows the mathematical definition directly:

```python
accum_new = accum + grad * grad
param_new = param - lr * grad / (np.sqrt(accum_new) + eps)
```

No input needs to be modified in place. The function creates new arrays for both returned values.

Because the accumulator is maintained element-wise, NumPy can apply the same update independently to every parameter element.
