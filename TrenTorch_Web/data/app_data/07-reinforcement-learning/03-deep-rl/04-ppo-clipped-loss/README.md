---
title: PPO Clipped Loss
name: rl-ppo-clipped-loss
difficulty: Advanced
tags: [rl, ppo, policy-gradient, clipping]
---

## Statement

Proximal Policy Optimization (PPO): policy gradient with clipped objective. Prevents destructive large policy updates while allowing reasonable improvements.

### The problem, from first principles

Standard policy gradients can have huge step sizes. PPO clips the objective to bound updates: if new policy improves too much, ignore the excess. Dramatically more stable than vanilla REINFORCE.

### From theory to code

Implement `ppo_loss(log_probs_new, log_probs_old, advantages, epsilon=0.2)` which:
- Computes probability ratio: r = exp(log_probs_new - log_probs_old)
- Unclipped: r * advantages
- Clipped: clip(r, 1-ε, 1+ε) * advantages
- Loss: -min(unclipped, clipped) mean
- Returns scalar loss

### Constraints

- Clipping preserves good improvements
- Prevents backtracking
- Typically ε in [0.1, 0.3]

### Hints

<details>
<summary>Hint 1: Probability ratio</summary>
r = exp(log p_new - log p_old) = p_new / p_old
</details>

<details>
<summary>Hint 2: Clipping</summary>
Clip ratio to [1-ε, 1+ε], element-wise
</details>

<details>
<summary>Hint 3: Loss is minimum</summary>
Take min of unclipped and clipped, then negate and average
</details>

## Theory

### PPO clipped objective

1. Compute old and new log probabilities
2. Ratio r = exp(log_new - log_old)
3. Unclipped: r * A
4. Clipped: clip(r, 1-ε, 1+ε) * A
5. L = -E[min(unclipped, clipped)]

### Intuition

If ratio >> 1, clipping ignores the huge advantage. If ratio << 1, clipping stops the huge loss. Takes conservative step.

## Explanation

PPO is the industry standard for policy gradient RL. Simple, stable, sample-efficient.
