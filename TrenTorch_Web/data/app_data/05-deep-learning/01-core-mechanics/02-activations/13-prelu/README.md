---
name: dl-activations-prelu
title: PReLU
tags: [deep-learning, activations]
difficulty: Beginner
---

## Statement

### The problem, from first principles

PReLU (Parametric ReLU) is like ReLU but with a learnable negative slope:

$$\text{prelu}(x, \alpha) = \begin{cases}
\alpha x & \text{if } x < 0 \\
x & \text{if } x \ge 0
\end{cases}$$

Where alpha can be learned during training. If alpha is fixed (e.g., 0.01), it is called LeakyReLU.

### From theory to code

Implement:

```python
prelu(x, alpha)
```

alpha can be a scalar or have the same shape as x.

### Constraints

- x can be any shape.
- alpha is a scalar or same shape as x.
- No input modification.
- Return a new array.

## Theory

PReLU generalizes ReLU by allowing a negative slope. If alpha = 0, it is ReLU. If alpha = 0.01, it is LeakyReLU. PReLU allows alpha to be trained.

## Explanation

```python
return np.where(x < 0, alpha * x, x)
```
