---
name: dl-training-adamax
title: Adamax
tags: [deep-learning, optimization, training]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Adam adapts learning rates per parameter using first and second moment estimates. Adamax is a variant that replaces the L2-norm-based second moment with an L-infinity norm operation.

Instead of dividing by sqrt(v), Adamax divides by the maximum of all past absolute gradients seen.

The updates are:

$$m_{\text{new}} = \beta_1 \cdot m + (1-\beta_1) \cdot \text{grad}$$

$$u_{\text{new}} = \max(\beta_2 \cdot u, |\text{grad}|)$$

$$\text{param}_{\text{new}} = \text{param} - \text{lr} \cdot \frac{m_{\text{new}}}{u_{\text{new}} + \text{eps}}$$

Where:
- m is the first moment (exponential moving average of gradients).
- u is the infinity norm (max absolute gradient observed, decayed).
- beta1 controls first moment decay (typically 0.9).
- beta2 controls infinity norm decay (typically 0.999).
- eps provides numerical stability.

### From theory to code

Implement:

```python
adamax_step(
    param,
    grad,
    m,
    u,
    lr,
    beta1,
    beta2,
    eps,
)
```

The function returns:

```python
(new_param, new_m, new_u)
```

The signature is provided in the editor.

First update the first moment estimate. Then update the infinity norm. Finally, compute the scaled update using both.

### Constraints

- param, grad, m, and u must have the same shape. Mismatch raises ValueError.
- lr must be greater than 0. Otherwise raise ValueError.
- beta1 and beta2 must both be in [0, 1). Otherwise raise ValueError.
- eps must be greater than 0. Otherwise raise ValueError.
- Inputs must not be modified.
- Return new arrays.
- m and u start at zeros.

### Hints

<details>
<summary>Hint 1</summary>

Compute m_new first as an exponential moving average of the gradient.

</details>

<details>
<summary>Hint 2</summary>

Compute u_new as the element-wise maximum of beta2 * u and the absolute gradient.

</details>

<details>
<summary>Hint 3</summary>

After computing m_new and u_new, scale the parameter update by m_new divided by (u_new + eps).

</details>

## Theory

### The simple version

Adamax is like Adam, but instead of tracking the root-mean-square of gradients, it tracks the largest absolute gradient component ever seen (with decay).

This can be more stable when gradients are sparse or very different in magnitude. The infinity norm is simpler to compute than an RMS.

### The formula

First update the first moment (mean of gradients):

$$m_{\text{new}} = \beta_1 \cdot m + (1-\beta_1) \cdot \text{grad}$$

Then update the infinity norm (max absolute gradient, decayed):

$$u_{\text{new}} = \max(\beta_2 \cdot u, |\text{grad}|)$$

Then update the parameter:

$$\text{param}_{\text{new}} = \text{param} - \text{lr} \cdot \frac{m_{\text{new}}}{u_{\text{new}} + \text{eps}}$$

The symbols mean:

- param is the current parameter.
- grad is the current gradient.
- m stores the first moment (mean of gradients).
- m_new is the updated first moment.
- u stores the infinity norm (max absolute gradient seen).
- u_new is the updated infinity norm.
- beta1 controls how much to keep the old mean vs. the new gradient.
- beta2 controls how much to keep the old max vs. the new gradient magnitude.
- eps provides numerical stability.
- lr is the learning rate.
- param_new is the updated parameter.

### Where it fits

Adamax is part of the Adam family of optimizers, which adapt the learning rate per parameter.

Adam uses a root-mean-square denominator. Adamax uses a max absolute denominator instead.

In PyTorch:

```python
torch.optim.Adamax(
    parameters,
    lr=learning_rate,
    betas=(beta1, beta2),
    eps=epsilon,
)
```

### Pros and cons

#### Pros

- Simpler to compute than Adam (no sqrt of second moment).
- Can be more stable on sparse gradients.
- Per-parameter adaptive learning rates.

#### Cons

- May not perform as well as Adam on dense problems.
- Introduces interactions between lr, beta1, beta2, and eps.
- Less commonly used than Adam in modern deep learning.

## Explanation

The solution follows three stages.

First, update the first moment:

```python
m_new = beta1 * m + (1 - beta1) * grad
```

This is the exponential moving average of the gradient, same as in Adam.

Next, update the infinity norm:

```python
u_new = np.maximum(beta2 * u, np.abs(grad))
```

This keeps the larger of the decayed previous max and the current gradient magnitude.

Finally, update the parameter:

```python
param_new = param - lr * m_new / (u_new + eps)
```

The parameter moves in the direction of the first moment, scaled by the ratio of the first moment to the infinity norm.

The implementation does not modify any input arrays. NumPy expressions create the returned arrays while preserving the originals.
