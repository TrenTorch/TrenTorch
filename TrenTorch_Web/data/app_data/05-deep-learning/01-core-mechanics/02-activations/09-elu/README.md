---
name: dl-activations-elu
title: ELU
tags: [deep-learning, activations]
difficulty: Beginner
---

## Statement

### The problem, from first principles

ELU (Exponential Linear Unit) is an activation that allows negative values for negative inputs, but with a smooth exponential form.

$$\text{elu}(x, \alpha) = \begin{cases}
\alpha(e^x - 1) & \text{if } x < 0 \\
x & \text{if } x \ge 0
\end{cases}$$

Typically alpha is 1.0. This can help reduce the vanishing gradient problem compared to ReLU.

### From theory to code

Implement:

```python
elu(x, alpha=1.0)
```

Returns output with negative values mapped through exponential, positive values unchanged.

### Constraints

- x can be any shape.
- alpha must be positive.
- No input modification.
- Return a new array.

## Theory

ELU allows negative outputs for negative inputs. For large negative x, the exponential approaches negative alpha. For positive x, it is the identity. This smoothness can improve training dynamics.

## Explanation

```python
return np.where(x < 0, alpha * (np.exp(x) - 1), x)
```
