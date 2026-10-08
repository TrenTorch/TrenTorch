---
name: research-sophia-clipped-step
title: 'Sophia: The Clipped Step'
tags: [research-papers, optimization, second-order]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Sophia (Liu et al., 2023) uses a diagonal Hessian estimate to set a per-coordinate step size, then clips each coordinate's step to a fixed range. The clip bounds the worst-case step even where the curvature estimate is poor.

### From theory to code

Implement `sophia_step(m, h, gamma, eps)`, the Hessian-scaled momentum step with per-entry clipping.

### Constraints

- The denominator is floored at eps.

### Hints

<details>
<summary>Hint 1</summary>

Divide the momentum by the larger of gamma times the Hessian and eps, then clip to minus one and one.

</details>

## Theory

### The simple version

Clipping means a bad curvature estimate can only make a bounded step, which is what makes a second-order method safe at scale.

### The formula

$$\Delta_i = \operatorname{clip}\!\left(\frac{m_i}{\max(\gamma h_i,\epsilon)},\,-1,\,1\right)$$

### How NumPy/PyTorch actually implements this

Sophia's paper reports the step is clipped on a sizable fraction of coordinates, which the next question measures.

## Explanation

Hand case: denominators are 0.5, so the ratios are 2 and -20, which clip to 1 and -1.
