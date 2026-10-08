---
name: research-adamw-effective-decay
title: 'AdamW: The Effective Decay per Step'
tags: [research-papers, optimization, weight-decay]
difficulty: Beginner
---

## Statement

### The problem, from first principles

With decoupled decay, each step multiplies the weights by a fixed factor. Over many steps that factor compounds, so the learning rate and decay together set how fast old weights are forgotten.

### From theory to code

Implement `effective_decay(lr, wd, steps)`, the fraction of weights remaining after pure decay.

### Constraints

- The shrink factor per step is one minus lr times wd.

### Hints

<details>
<summary>Hint 1</summary>

Raise one minus lr times wd to the number of steps.

</details>

## Theory

### The simple version

Compounding the per-step factor gives a closed form, which helps pick wd so weights decay on a useful time scale.

### The formula

$$\text{remaining} = (1-\eta\lambda)^{T}$$

### How NumPy/PyTorch actually implements this

Weight decay schedules tune lr and wd jointly for this reason.

## Explanation

The test with 0.9025 checks two steps of 0.95 each, the compounding in the formula.
