---
title: Target Networks in DQN
name: rl-target-networks
difficulty: Advanced
tags: [rl, dqn, deep-learning, stability]
---

## Statement

Target networks: separate frozen network for computing TD targets. Breaks correlations between consecutive TD targets, stabilizing training.

### The problem, from first principles

In DQN, Q-network updates the target used to compute the loss (bootstrapping). This creates moving targets, causing instability. Solution: use a separate frozen network to compute targets, update it periodically.

### From theory to code

Implement `update_target_network(network, target_network, tau=0.001)` which:

- Performs soft update: target_params = (1 - τ) * target_params + τ * network_params
- Or hard update if τ=1: target_params = network_params
- Returns updated target network

### Constraints

- Typically τ small (0.001) for soft updates
- Hard update every C steps is alternative
- Must match architecture of main network

### Hints

<details>
<summary>Hint 1: Soft update</summary>
target = (1 - tau) * target + tau * main
</details>

<details>
<summary>Hint 2: Parameter iteration</summary>
Apply to each parameter independently
</details>

<details>
<summary>Hint 3: No gradient needed</summary>
Target network params don't require gradients
</details>

## Theory

### Target network algorithm

1. Maintain two identical networks: main and target
2. Main network trained normally via experience replay
3. Target network updated periodically (soft or hard)
4. TD target computed using target network (frozen)
5. Main network fits to this target

### Stability gain

Decorrelates TD targets from network updates. Makes bootstrapping safer.

## Explanation

Target networks are essential for DQN stability. Without them, DQN diverges on complex tasks.
