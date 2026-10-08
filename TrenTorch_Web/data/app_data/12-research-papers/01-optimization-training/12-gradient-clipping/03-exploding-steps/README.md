---
name: research-clip-exploding-steps
title: 'Gradient Clipping: Counting Exploding Steps'
tags: [research-papers, optimization, stability]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Clipping only helps if you know how often it fires. Counting the steps whose gradient norm exceeds the threshold tells you whether the threshold is set too low or the run is unstable.

### From theory to code

Implement `exploding_steps(grad_norms, threshold)`, the count of steps above the threshold.

### Constraints

- Strictly greater than the threshold counts.

### Hints

<details>
<summary>Hint 1</summary>

Count the norms that are larger than the threshold.

</details>

## Theory

### The simple version

A rising count is an early warning of divergence, and it is a cheap diagnostic to log during training.

### The formula

$$\#\{t : \lVert g_t\rVert > \tau\}$$

### How NumPy/PyTorch actually implements this

Training loops log this count alongside loss and learning rate.

## Explanation

Hand case: of 0.5, 3.0, 2.5, 1.0 with threshold 2, two exceed it.
