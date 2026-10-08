---
name: research-adamw-decoupled-update
title: 'AdamW: The Decoupled Update'
tags: [research-papers, optimization, weight-decay]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Adam's L2 regularization adds the decay term to the gradient, so it is rescaled by the adaptive denominator. AdamW (Loshchilov & Hutter, 2017) applies decay directly to the weights, which restores the regularization meaning.

### From theory to code

Implement `adamw_update(w, m_hat, v_hat, lr, wd, eps)`, the Adam step plus a decoupled decay term.

### Constraints

- Decay is scaled by the learning rate and not by the second moment.

### Hints

<details>
<summary>Hint 1</summary>

Compute the Adam direction, then subtract lr times wd times the current weights.

</details>

## Theory

### The simple version

Keeping decay out of the adaptive scaling means every weight shrinks by the same fraction per step, which is what weight decay is supposed to do.

### The formula

$$w_{t+1} = w_t - \eta\left(\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon} + \lambda w_t\right)$$

### How NumPy/PyTorch actually implements this

PyTorch's `AdamW` applies `p.mul_(1 - lr * wd)` before the Adam update, the same decoupling.

## Explanation

The test with zero gradient shows the decay alone shrinks the weights, which the L2-in-gradient form cannot do under Adam scaling.
