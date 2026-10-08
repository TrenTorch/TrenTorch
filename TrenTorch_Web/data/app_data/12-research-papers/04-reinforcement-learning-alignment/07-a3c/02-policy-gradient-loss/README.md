---
name: research-a3c-policy-gradient-loss
title: 'A3C: The Policy Gradient Loss'
tags: [research-papers, reinforcement-learning, actor-critic, asynchronous]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The policy-gradient update raises the log-probability of actions that had positive advantage. Minimizing the negative of logp times advantage does exactly that when used with an optimizer.

### From theory to code

Implement `policy_gradient_loss(logp, adv)`, returning the negated mean of `logp * adv`.

### Constraints

- Returns a Python float.

### Hints

<details>
<summary>Hint 1</summary>

Multiply, average, negate.

</details>

## Theory

### The simple version

Gradient descent on this loss pushes probability toward good actions and away from bad ones, weighted by how good or bad they were.

### The formula

$$\mathcal{L}_{\pi} = -\frac{1}{N}\sum_i \log\pi_\theta(a_i\mid s_i)\,\hat A_i$$

### How NumPy/PyTorch actually implements this

A3C and most actor-critic codes compute this loss on each rollout before summing it with the value and entropy terms.

## Explanation

Treating the advantage as a constant weight is what makes this a standard surrogate loss for autograd.
