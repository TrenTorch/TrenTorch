---
name: research-adafactor-relative-step
title: 'Adafactor: The Relative Step Size'
tags: [research-papers, optimization, memory]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Adafactor can run without a learning rate by using a relative step that decays with the square root of the step count, capped at a fixed maximum.

### From theory to code

Implement `relative_step(t)`, the capped inverse-square-root schedule.

### Constraints

- The cap is 0.01.

### Hints

<details>
<summary>Hint 1</summary>

Take the minimum of 0.01 and one over the square root of the step.

</details>

## Theory

### The simple version

The cap keeps early steps from being too large, and the inverse-square-root decay keeps late steps small without a hand-tuned schedule.

### The formula

$$\rho_t = \min\left(10^{-2}, \frac{1}{\sqrt t}\right)$$

### How NumPy/PyTorch actually implements this

The Adafactor implementation computes this step inside its update when the learning rate is unset.

## Explanation

At t = 40000 the inverse-square-root term is 0.005, below the cap.
