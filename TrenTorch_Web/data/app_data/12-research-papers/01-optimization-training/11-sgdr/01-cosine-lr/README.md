---
name: research-sgdr-cosine-lr
title: 'SGDR: The Cosine Learning Rate'
tags: [research-papers, optimization, learning-rate-schedule, restarts]
difficulty: Beginner
---

## Statement

### The problem, from first principles

SGDR (Loshchilov & Hutter, 2016) anneals the learning rate along half a cosine curve within each cycle. Restarting it to the maximum at the start of each cycle lets the optimizer re-explore.

### From theory to code

Implement `cosine_lr(t_cur, T_i, eta_min, eta_max)`, the cosine-annealed learning rate.

### Constraints

- Use the position within the current cycle.

### Hints

<details>
<summary>Hint 1</summary>

Take the cosine of pi times the fraction of the cycle completed, map it from minus one to one onto the bounds.

</details>

## Theory

### The simple version

The cosine starts flat near the maximum and ends flat near the minimum, so the rate changes gently at both ends of the cycle.

### The formula

$$\eta_t = \eta_{\min} + \tfrac12(\eta_{\max}-\eta_{\min})\left(1+\cos\frac{\pi t_{\text{cur}}}{T_i}\right)$$

### How NumPy/PyTorch actually implements this

Schedulers implement this as `CosineAnnealingLR` with a per-cycle restart.

## Explanation

At half the cycle the cosine is zero, so the rate is the midpoint of the bounds.
