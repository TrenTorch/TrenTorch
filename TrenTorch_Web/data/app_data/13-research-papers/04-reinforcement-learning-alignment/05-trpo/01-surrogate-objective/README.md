---
name: research-trpo-surrogate
title: 'TRPO: The Surrogate Objective'
tags: [research-papers, reinforcement-learning, policy-gradient, trust-region]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

TRPO (Schulman et al., 2015) improves a policy by maximizing the advantage of new actions, weighted by how much more likely the new policy makes them. The ratio is an importance weight that corrects for sampling from the old policy.

### From theory to code

Implement `surrogate_objective(ratio, advantage)`, returning the mean of `ratio * advantage`.

### Constraints

- The ratio of 1 means the new policy equals the old one.

### Hints

<details>
<summary>Hint 1</summary>

Multiply element-wise and take the mean.

</details>

## Theory

### The simple version

At the old policy the surrogate equals the true improvement, so maximizing it locally is a valid step. The trust region constraint keeps the policy close enough for that approximation to hold.

### The formula

$$L(\theta) = \mathbb{E}\left[\frac{\pi_\theta(a\mid s)}{\pi_{\theta_{\text{old}}}(a\mid s)}\,\hat A\right]$$

### How NumPy/PyTorch actually implements this

Policy-gradient libraries compute this surrogate per batch and then add the KL constraint or clipping.

## Explanation

The expectation is estimated with the sample mean over a batch of rollouts from the old policy.
