---
name: research-sophia-clip-fraction
title: 'Sophia: How Often Steps Are Clipped'
tags: [research-papers, optimization, second-order]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Sophia reports how often its per-coordinate steps hit the clip. Tracking this fraction shows whether the curvature estimate is too small, which causes frequent clipping.

### From theory to code

Implement `clip_fraction(ratios)`, the share of coordinates whose ratio magnitude reaches one.

### Constraints

- A ratio of exactly one counts as clipped.

### Hints

<details>
<summary>Hint 1</summary>

Take the absolute values, compare with one, and average the boolean result.

</details>

## Theory

### The simple version

A high clip fraction means the Hessian estimate is too small for the momentum, so gamma or the refresh schedule needs adjusting.

### The formula

$$f = \frac{1}{d}\sum_i \mathbf 1\{|r_i| \ge 1\}$$

### How NumPy/PyTorch actually implements this

Training logs report this statistic as a diagnostic for the second-order estimate.

## Explanation

Hand case: |2| and |-5| are at least one, so two of four entries are clipped.
