---
name: research-a3c-n-step-return
title: 'A3C: The n-Step Return'
tags: [research-papers, reinforcement-learning, actor-critic, asynchronous]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A3C (Mnih et al., 2016) runs many workers in parallel, and each collects a short rollout of n steps before updating. The learning target for that rollout is an n-step return: the rewards actually seen, plus a bootstrapped value for the state at the end.

### From theory to code

Implement `n_step_return(rewards, bootstrap, gamma)`, returning the discounted sum of the rewards plus the discounted bootstrap value.

### Constraints

- Use the bootstrap value as the starting point of the backward pass.

### Hints

<details>
<summary>Hint 1</summary>

Start from `bootstrap`, and for each reward from last to first set `G = r + gamma * G`.

</details>

## Theory

### The simple version

Longer rollouts reduce the bias from the value estimate and speed up credit assignment, while the bootstrap keeps variance bounded.

### The formula

$$R_t^{(n)} = \sum_{k=0}^{n-1}\gamma^k r_{t+k} + \gamma^n V(s_{t+n})$$

### How NumPy/PyTorch actually implements this

Asynchronous actor-critic implementations compute this target at the end of each local rollout before pushing gradients.

## Explanation

The backward recursion computes the same n-step sum without storing powers of gamma.
