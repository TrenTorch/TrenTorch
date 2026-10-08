---
name: research-ppo-total-loss
title: 'PPO: The Combined Training Loss'
tags: [research-papers, reinforcement-learning, policy-gradient, ppo]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

PPO optimizes three things together: the clipped policy objective, the value function fit, and an entropy bonus that keeps the policy from collapsing early. The paper combines them with two coefficients into one scalar objective.

### From theory to code

Implement `ppo_total_loss(clip_obj, vf_loss, entropy, c1, c2)`, returning the negated combined objective.

### Constraints

- Optimizers minimize, so the objective is negated.

### Hints

<details>
<summary>Hint 1</summary>

Compute `clip_obj - c1 * vf_loss + c2 * entropy`, then return its negative.

</details>

## Theory

### The simple version

The value term keeps the critic accurate for the advantage estimates, and the entropy term rewards spread-out action distributions. Negating turns the maximization into a loss to minimize.

### The formula

$$\mathcal{L} = -\big(L^{\text{CLIP}} - c_1\,L^{\text{VF}} + c_2\,S[\pi_\theta]\big)$$

### How NumPy/PyTorch actually implements this

Actor-critic trainers sum these terms into one loss and call `backward` once per minibatch.

## Explanation

The paper's coefficients are small constants; the sign of each term follows from maximizing the combined objective.
