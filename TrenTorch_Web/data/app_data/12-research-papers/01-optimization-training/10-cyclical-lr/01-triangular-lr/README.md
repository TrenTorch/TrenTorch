---
name: research-clr-triangular-lr
title: 'Cyclical Learning Rates: The Triangular Schedule'
tags: [research-papers, optimization, learning-rate-schedule]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Smith (2015) cycles the learning rate between a lower and upper bound instead of decaying it monotonically. A triangular wave goes up and down each cycle, which lets the model escape poor regions.

### From theory to code

Implement `triangular_lr(it, base, max_lr, step)`, the triangular cyclical rate.

### Constraints

- Each half-cycle takes `step` iterations.

### Hints

<details>
<summary>Hint 1</summary>

Find which cycle the iteration is in, measure its distance from the peak, and interpolate linearly between the bounds.

</details>

## Theory

### The simple version

The rate rises and falls on a fixed schedule, so one can find a good range by watching the loss across a cycle.

### The formula

$$\eta_t = \eta_{\min} + (\eta_{\max}-\eta_{\min})\max\big(0,\,1-|t/s - 2c + 1|\big)$$

### How NumPy/PyTorch actually implements this

Deep learning libraries implement this as a cyclic scheduler with the same triangle.

## Explanation

Hand case with step 4: iteration 0 gives the base, iteration 2 gives halfway, iteration 4 gives the max.
