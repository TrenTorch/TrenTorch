---
name: dl-activations-hardtanh
title: Hardtanh
tags: [deep-learning, activations]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Hardtanh is a piecewise linear activation that bounds input to the range [-1, 1].

$$\text{hardtanh}(x) = \begin{cases}
-1 & \text{if } x < -1 \\
x & \text{if } -1 \le x \le 1 \\
1 & \text{if } x > 1
\end{cases}$$

It is even simpler than hard sigmoid. Used in some quantization schemes and mobile models.

### From theory to code

Implement:

```python
hardtanh(x)
```

Returns output bounded in [-1, 1].

### Constraints

- x can be any shape.
- No input modification.
- Return a new array.

### Hints

<details>
<summary>Hint 1</summary>

Use np.clip with bounds -1 and 1.

</details>

## Theory

Hardtanh clips values to [-1, 1]. It is the simplest form of bounded activation and has near-zero gradient outside the active region.

## Explanation

```python
return np.clip(x, -1.0, 1.0)
```
