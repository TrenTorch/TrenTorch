---
name: research-gae-td-residuals
title: 'GAE: One-Step TD Residuals'
tags: [research-papers, reinforcement-learning, policy-gradient, advantage]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The advantage of an action is how much better it turned out than the value function expected. A single step of that comparison is the TD residual: the observed reward plus the discounted next value, minus the current value.

### From theory to code

Implement `td_residuals(rewards, values, gamma, last_value)`, returning the one-step residual at each time step.

### Constraints

- The value after the last step is `last_value`.

### Hints

<details>
<summary>Hint 1</summary>

Shift the values by one step to get each next value, then compute `r + gamma * next - value`.

</details>

## Theory

### The simple version

A positive residual means the step was better than predicted, which makes the action worth reinforcing. These residuals are the raw material that GAE combines over many steps.

### The formula

$$\delta_t = r_t + \gamma\,V(s_{t+1}) - V(s_t)$$

### How NumPy/PyTorch actually implements this

PPO implementations compute this vector with a vectorized shift over the rollout buffer.

## Explanation

The residual is a one-step advantage estimate: low variance, but biased by the value function.
