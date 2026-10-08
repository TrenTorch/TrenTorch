---
name: research-swish-forward
title: 'Swish: A Self-Gated Activation'
tags: [research-papers, activation, swish]
difficulty: Beginner
---

## Statement

### The problem, from first principles

ReLU is cheap but has a hard kink at zero. The Swish paper (Ramachandran, Zoph & Le, 2017) found by automated search that `x * sigmoid(x)` often beats ReLU on deep networks, because the input gates itself smoothly.

### From theory to code

Implement `swish(x, beta)`, which returns `x * sigmoid(beta * x)`.

### Constraints

- With `beta = 1` this is the standard Swish (also called SiLU).

### Hints

<details>
<summary>Hint 1</summary>

The sigmoid is `1 / (1 + exp(-beta * x))`; multiply it by `x`.

</details>

## Theory

### The simple version

The input decides how much of itself to pass, through a smooth gate. For large positive inputs the gate is about 1 and the function is linear; for large negative inputs it is about 0.

### The formula

$$\text{Swish}(x) = x\,\sigma(\beta x) = \frac{x}{1 + e^{-\beta x}}$$

### How NumPy/PyTorch actually implements this

`torch.nn.functional.silu(x)` computes Swish with `beta = 1`.

## Explanation

The sigmoid is the logistic function written with `np.exp`. Larger `beta` makes the gate sharper and the function closer to ReLU.
