---
name: research-ppo-objective-batch
title: 'PPO: The Clipped Objective Over a Batch'
tags: [research-papers, reinforcement-learning, policy-gradient, ppo]
difficulty: Advanced
---

## Statement

### The problem, from first principles

The clipped surrogate is the heart of PPO. Each sample contributes the smaller of the raw and clipped weighted advantage, and the batch objective is their average.

### From theory to code

Implement `ppo_objective(ratios, advantages, eps)`, the batch mean of the element-wise clipped minimum.

### Constraints

- `eps` is the clip range, typically 0.2.

### Hints

<details>
<summary>Hint 1</summary>

Compute `ratios * advantages` and `clip(ratios) * advantages`, take the element-wise minimum, then average.

</details>

## Theory

### The simple version

Clipping removes the incentive to push a ratio beyond the band, while the minimum keeps the objective pessimistic when an update would be harmful.

### The formula

$$L^{\text{CLIP}}(\theta) = \mathbb{E}_t\Big[\min\big(r_t(\theta)\hat A_t,\ \operatorname{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat A_t\big)\Big]$$

### How NumPy/PyTorch actually implements this

PPO trainers in RL libraries compute this exact expression on each minibatch.

## Explanation

This is the batch version of the per-sample clipped surrogate used in the InstructGPT question, with the average taken over the rollout.
