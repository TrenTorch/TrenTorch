---
name: research-dqn-td-target
title: 'DQN: The Bellman Target'
tags: [research-papers, reinforcement-learning, deep-q-learning]
difficulty: Beginner
---

## Statement

### The problem, from first principles

DQN (Mnih et al., 2013/2015) learns an action-value function by regressing it toward a bootstrapped target: the reward plus the discounted best value at the next state. The target is what the Q-network is pulled toward on every update.

### From theory to code

Implement `td_target(r, gamma, max_next_q, done)`, returning the one-step Bellman target.

### Constraints

- Terminal transitions do not bootstrap.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the next-state value by `gamma` and by `(1 - done)`, then add the reward.

</details>

## Theory

### The simple version

The target is the reward you got plus your best estimate of what follows. Cutting the bootstrap at the end of an episode stops value from leaking past the last state.

### The formula

$$y = r + \gamma\,(1 - d)\,\max_{a'} Q_{\bar\theta}(s', a')$$

### How NumPy/PyTorch actually implements this

Libraries such as Stable-Baselines3 compute this target in one vectorized line inside the DQN update.

## Explanation

The max is taken with the slow-moving target network, which stabilizes learning compared with using the online network.
