---
name: dl-activations-softplus
title: Softplus
tags: [deep-learning, activations]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Softplus is a smooth approximation to ReLU:

$$\text{softplus}(x, \beta=1) = \frac{1}{\beta} \log(1 + e^{\beta x})$$

It is always positive and smooth everywhere, unlike ReLU which has a kink at 0.

### From theory to code

Implement:

```python
softplus(x, beta=1.0)
```

### Constraints

- x can be any shape.
- beta > 0.
- No input modification.
- Return a new array.

## Theory

Softplus is the smooth counterpart to ReLU. For large x, softplus(x) ~ x. For large negative x, softplus(x) ~ 0. The transition is smooth.

## Explanation

```python
return (1.0 / beta) * np.log(1.0 + np.exp(beta * x))
```

For numerical stability, large beta * x can overflow. A more stable form handles this:

```python
return np.where(
    x > 20.0 / beta,
    x,
    (1.0 / beta) * np.log(1.0 + np.exp(beta * x))
)
```
