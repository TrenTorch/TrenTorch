---
name: research-swish-derivative
title: 'Swish: The Derivative With Beta'
tags: [research-papers, activation, swish]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Training needs the gradient of Swish. Its derivative combines the gate and the input's own contribution, so it stays nonzero for negative inputs, unlike ReLU's zero gradient there.

### From theory to code

Implement `swish_derivative(x, beta)`, returning `s + beta * x * s * (1 - s)` with `s = sigmoid(beta * x)`.

### Constraints

- Must match a numerical derivative of `swish`.

### Hints

<details>
<summary>Hint 1</summary>

Write `s = sigmoid(beta * x)`, then apply the product rule to `x * s`.

</details>

## Theory

### The simple version

The derivative has two parts: the gate `s` itself, and the input's effect on the gate. Both contribute to the gradient, which is why Swish keeps learning signal near zero and below.

### The formula

$$\frac{d}{dx}\big[x\,\sigma(\beta x)\big] = \sigma(\beta x) + \beta\,x\,\sigma(\beta x)\big(1 - \sigma(\beta x)\big)$$

### How NumPy/PyTorch actually implements this

Autograd gives this derivative for `torch.nn.functional.silu`; the explicit form is useful for checking gradients.

## Explanation

`s * (1 - s)` is the sigmoid's own derivative. Writing `s` once keeps the code short and avoids recomputing the exponential.
