---
name: research-gae-advantages
title: 'GAE: Combining Residuals With Lambda'
tags: [research-papers, reinforcement-learning, policy-gradient, advantage]
difficulty: Advanced
---

## Statement

### The problem, from first principles

GAE (Schulman et al., 2016) blends many one-step advantage estimates with an exponential weight. The parameter lambda trades bias against variance: lambda 0 uses only one step, and lambda 1 uses the full Monte Carlo return.

### From theory to code

Implement `gae_advantages(deltas, gamma, lam)`, computing the exponentially weighted sum of future residuals.

### Constraints

- `lam` between 0 and 1.

### Hints

<details>
<summary>Hint 1</summary>

Walk the residuals from last to first, keeping a running sum scaled by `gamma * lam`.

</details>

## Theory

### The simple version

Each advantage is the residual now plus a discounted version of the advantage one step later, so the recursion gives every step its exponentially weighted future.

### The formula

$$\hat A_t = \sum_{k=0}^{\infty} (\gamma\lambda)^k\,\delta_{t+k} \quad\Longleftrightarrow\quad \hat A_t = \delta_t + \gamma\lambda\,\hat A_{t+1}$$

### How NumPy/PyTorch actually implements this

PPO implementations, including Stable-Baselines3, compute GAE with a reversed loop over the buffer.

## Explanation

The backward recursion computes the infinite sum exactly with one pass over the rollout.
