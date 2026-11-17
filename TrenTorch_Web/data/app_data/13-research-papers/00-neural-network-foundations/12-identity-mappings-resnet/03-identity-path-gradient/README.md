---
name: research-residual-gradient
title: 'Identity Mappings in ResNet: The Gradient Through the Shortcut'
tags: [research-papers, architecture, resnet]
difficulty: Advanced
---

## Statement

### The problem, from first principles

The paper's central argument is about the backward pass. With an identity shortcut, the gradient reaching earlier layers always includes a copy of the upstream gradient, so it cannot vanish through the shortcut alone.

### From theory to code

Implement `identity_path_gradient(grad_out, jac_f)`, returning `grad_out (I + J_F)` for a row-vector gradient.

### Constraints

- `jac_f` is the `(D, D)` Jacobian of the residual branch.

### Hints

<details>
<summary>Hint 1</summary>

Write `grad_out @ (I + jac_f)`, which equals `grad_out + grad_out @ jac_f`.

</details>

## Theory

### The simple version

The derivative of `x + F(x)` is `I + dF/dx`. The identity term guarantees a nonzero path even when the residual branch's Jacobian is small or zero.

### The formula

$$\frac{\partial L}{\partial x} = \frac{\partial L}{\partial y}\left(I + \frac{\partial \mathcal{F}}{\partial x}\right)$$

### How NumPy/PyTorch actually implements this

Autograd on a residual block produces exactly this sum; the explicit form makes the shortcut's role visible.

## Explanation

Row-vector gradients multiply on the right, so the identity term appears as `grad_out` itself. This is the term that keeps the gradient alive through deep stacks.
