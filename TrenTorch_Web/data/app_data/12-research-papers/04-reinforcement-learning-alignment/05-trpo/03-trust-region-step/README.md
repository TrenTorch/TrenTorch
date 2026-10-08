---
name: research-trpo-step-size
title: 'TRPO: The Trust-Region Step Size'
tags: [research-papers, reinforcement-learning, policy-gradient, trust-region]
difficulty: Advanced
---

## Statement

### The problem, from first principles

TRPO takes the largest step whose KL stays within the limit. Approximating the KL by a quadratic around the current policy turns that into a closed-form step length, which is the scaling the paper applies to its natural gradient direction.

### From theory to code

Implement `trust_region_step_size(delta, quad)`, returning `sqrt(2 delta / quad)`.

### Constraints

- `quad` is positive.

### Hints

<details>
<summary>Hint 1</summary>

Solve the quadratic constraint `0.5 * beta^2 * quad = delta` for `beta`.

</details>

## Theory

### The simple version

A flatter direction (small curvature) allows a longer step before the KL limit is reached. The step length adapts to the geometry of the policy.

### The formula

$$\beta = \sqrt{\frac{2\delta}{g^\top F^{-1} g}}$$

### How NumPy/PyTorch actually implements this

Implementations compute the same scalar from a conjugate-gradient estimate of `g^T F^{-1} g`.

## Explanation

The natural gradient direction scaled by this beta lands on the boundary of the KL ball of radius delta.
