---
name: research-clr-range-test
title: 'Cyclical Learning Rates: The LR Range Test'
tags: [research-papers, optimization, learning-rate-schedule]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The LR range test (Smith, 2015) raises the learning rate exponentially over a short run and records the loss. The rate where the loss falls fastest is a good choice for the bounds of the cyclical schedule.

### From theory to code

Implement `lr_range_test(it, min_lr, gamma)`, the geometrically increasing learning rate.

### Constraints

- Iterations start at zero.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the starting rate by the growth factor raised to the iteration number.

</details>

## Theory

### The simple version

A geometric sweep covers several orders of magnitude in few steps, so one short run finds the useful range.

### The formula

$$\eta_t = \eta_{\min}\,\gamma^{t}$$

### How NumPy/PyTorch actually implements this

Practitioners plot loss against this learning rate and pick the bounds from the descending part of the curve.

## Explanation

Hand case: 1e-4 times 2 cubed is 8e-4.
