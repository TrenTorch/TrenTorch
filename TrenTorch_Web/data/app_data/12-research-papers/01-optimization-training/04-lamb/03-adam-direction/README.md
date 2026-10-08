---
name: research-lamb-adam-direction
title: 'LAMB: The Adam Direction'
tags: [research-papers, optimization, large-batch, adam]
difficulty: Beginner
---

## Statement

### The problem, from first principles

LAMB's direction is Adam's normalized moment ratio, plus decoupled weight decay on the weights. It is the quantity whose norm the trust ratio compares against the weights.

### From theory to code

Implement `lamb_direction(m_hat, v_hat, w, wd, eps)`, the Adam direction with decay.

### Constraints

- The decay term uses the weights themselves.

### Hints

<details>
<summary>Hint 1</summary>

Divide the first moment by the square root of the second plus eps, then add wd times the weights.

</details>

## Theory

### The simple version

Adam's normalization keeps each coordinate's step well-scaled; the decay term keeps the weights from growing without bound.

### The formula

$$r_t = \frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon} + \lambda w_t$$

### How NumPy/PyTorch actually implements this

Implementations compute this direction per parameter tensor before the trust-ratio scaling.

## Explanation

The hand case gives 1 + 0.5 * 2 = 2.
