---
name: dl-activations-softsign
title: Softsign
tags: [deep-learning, activations]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Softsign is a smooth activation that maps input to (-1, 1):

$$\text{softsign}(x) = \frac{x}{1 + |x|}$$

It is smoother than tanh and simpler to compute.

### From theory to code

Implement:

```python
softsign(x)
```

### Constraints

- x can be any shape.
- No input modification.
- Return a new array.

## Theory

Softsign is a smooth alternative to tanh. Output range is (-1, 1). It can be easier to optimize than tanh in some cases.

## Explanation

```python
return x / (1.0 + np.abs(x))
```
