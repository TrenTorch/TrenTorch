---
name: research-dim-softplus
title: 'Deep InfoMax: The Softplus Function'
tags: [research-papers, unsupervised, mutual-information, representation]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The softplus is a smooth version of ReLU, and it appears throughout mutual information estimators. Written naively, exp overflows for large inputs, so a stable form is needed.

### From theory to code

Implement `softplus(x)`, returning `log(1 + exp(x))`.

### Constraints

- Avoid computing `exp(x)` directly for large x.

### Hints

<details>
<summary>Hint 1</summary>

Use `np.logaddexp(0, x)`, which evaluates the same quantity stably.

</details>

## Theory

### The simple version

Softplus is always positive and approaches x for large x and zero for very negative x. Its derivative is the sigmoid, which makes it a natural smooth gate in estimators.

### The formula

$$\operatorname{softplus}(x) = \log(1 + e^x)$$

### How NumPy/PyTorch actually implements this

`torch.nn.functional.softplus` implements this with a threshold for large inputs.

## Explanation

The derivative is the logistic sigmoid, so the gradient of the mutual information estimate reuses sigmoid-like terms.
