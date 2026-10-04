---
name: dl-activations-selu
title: SELU
tags: [deep-learning, activations]
difficulty: Beginner
---

## Statement

### The problem, from first principles

SELU (Scaled ELU) is ELU scaled by a factor to achieve self-normalizing properties in deep networks.

$$\text{selu}(x) = \lambda \begin{cases}
\alpha(e^x - 1) & \text{if } x < 0 \\
x & \text{if } x \ge 0
\end{cases}$$

Where lambda and alpha are fixed constants (typically lambda ~ 1.0507, alpha ~ 1.6733).

### From theory to code

Implement:

```python
selu(x)
```

Uses standard SELU constants.

### Constraints

- x can be any shape.
- No input modification.
- Return a new array.

## Theory

SELU is designed to self-normalize activations in deep networks. The scaling factors ensure that outputs have zero mean and unit variance under certain conditions.

## Explanation

```python
LAMBDA = 1.0507
ALPHA = 1.6733
return LAMBDA * np.where(x < 0, ALPHA * (np.exp(x) - 1), x)
```
