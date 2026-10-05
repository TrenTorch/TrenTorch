---
name: research-gelu-derivative
title: 'GELU: The Derivative'
tags: [research-papers, activation, gelu]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Training needs the gradient of GELU, not just its value. Because GELU is a product of `x` and the Gaussian CDF, the derivative has a simple closed form that backpropagation uses directly.

### From theory to code

Implement `gelu_derivative(x)`, returning `Phi(x) + x * phi(x)` element-wise.

### Constraints

- `phi(x) = exp(-x^2 / 2) / sqrt(2 pi)`.

### Hints

<details>
<summary>Hint 1</summary>

Apply the product rule to `x * Phi(x)`: the derivative is `Phi(x)` plus `x` times the density `phi(x)`.

</details>

## Theory

### The simple version

Near zero the derivative is about one half; for large positive inputs it approaches one, and for large negative inputs it approaches zero, mirroring the function itself.

### The formula

$$\frac{d}{dx}\big[x\,\Phi(x)\big] = \Phi(x) + x\,\phi(x), \qquad \phi(x) = \frac{1}{\sqrt{2\pi}}e^{-x^2/2}$$

### How NumPy/PyTorch actually implements this

Autograd computes this automatically for `torch.nn.functional.gelu`; writing it out checks the backward pass by hand.

## Explanation

The density `phi` is the standard normal PDF. The derivative is smooth everywhere, which is one reason GELU trains smoothly compared with ReLU.
