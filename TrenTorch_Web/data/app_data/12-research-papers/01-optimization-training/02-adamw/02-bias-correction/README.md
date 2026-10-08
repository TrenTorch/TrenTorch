---
name: research-adamw-bias-correction
title: 'AdamW: Bias Correction'
tags: [research-papers, optimization, adam]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Adam's moment estimates start at zero, so they underestimate the true average early in training. AdamW keeps Adam's bias correction, which divides each moment by one minus its decay raised to the step count.

### From theory to code

Implement `bias_corrected(m, v, beta1, beta2, t)`, returning the corrected first and second moments.

### Constraints

- The step count starts at 1.

### Hints

<details>
<summary>Hint 1</summary>

Divide the first moment by one minus beta1 to the t, and the second by one minus beta2 to the t.

</details>

## Theory

### The simple version

Early on, the moments are averages over very few gradients and are biased toward zero. Dividing by the missing mass undoes that bias, and the effect fades as t grows.

### The formula

$$\hat m_t = \frac{m_t}{1-\beta_1^t},\qquad \hat v_t = \frac{v_t}{1-\beta_2^t}$$

### How NumPy/PyTorch actually implements this

Optimizer implementations keep the step counter and apply these two divisions before the parameter update.

## Explanation

The second hand value is 0.19 over 0.19, which checks the division at step two.
