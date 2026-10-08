---
name: research-lars-trust-ratio
title: 'LARS: The Layer Trust Ratio'
tags: [research-papers, optimization, large-batch]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

LARS (You et al., 2017) lets each layer take a step proportional to how large its weights are relative to its gradient. The layer's learning rate is scaled by this trust ratio, so large-batch training stays stable across layers.

### From theory to code

Implement `trust_ratio(w, g, eta, wd)`, the layer-wise local learning-rate multiplier.

### Constraints

- The denominator includes the decay term.

### Hints

<details>
<summary>Hint 1</summary>

Take the weight norm, multiply by eta, and divide by the gradient norm plus wd times the weight norm.

</details>

## Theory

### The simple version

A layer with small gradients relative to its weights gets a larger step, and vice versa. The trust ratio keeps each layer's update a fixed fraction of its weight size.

### The formula

$$\lambda_\ell = \eta\,\frac{\lVert w_\ell\rVert}{\lVert \nabla L(w_\ell)\rVert + \beta\lVert w_\ell\rVert}$$

### How NumPy/PyTorch actually implements this

Large-batch training frameworks compute one norm pair per parameter tensor, which is what LARS does.

## Explanation

The hand case uses ||w|| = 5 and ||g|| = 1, so the ratio is 0.5 times 5.
