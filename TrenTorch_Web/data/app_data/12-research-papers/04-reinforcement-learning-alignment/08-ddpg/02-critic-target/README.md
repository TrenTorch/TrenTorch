---
name: research-ddpg-critic-target
title: 'DDPG: The Critic Target'
tags: [research-papers, reinforcement-learning, continuous-control, actor-critic]
difficulty: Beginner
---

## Statement

### The problem, from first principles

DDPG learns a deterministic actor and a critic that scores actions. The critic is trained toward a one-step target that uses the target actor's action and the target critic's value at the next state.

### From theory to code

Implement `ddpg_critic_target(r, gamma, done, q_next)`, the one-step critic target.

### Constraints

- No bootstrap after a terminal state.

### Hints

<details>
<summary>Hint 1</summary>

Compute `r + gamma * (1 - done) * q_next`.

</details>

## Theory

### The simple version

The target is built from the slow target networks, so the regression target changes gradually even though the critic is trained every step.

### The formula

$$y = r + \gamma\,(1 - d)\,Q_{\theta'}\big(s', \mu_{\phi'}(s')\big)$$

### How NumPy/PyTorch actually implements this

Continuous-control implementations, such as in Stable-Baselines3, compute this target inside the critic update.

## Explanation

This is the Bellman target for a deterministic policy: the next action is the target actor's output, not a maximization.
