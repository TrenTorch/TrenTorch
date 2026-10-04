---
title: Monte Carlo with Exploring Starts
name: rl-mc-exploring-starts
difficulty: Intermediate
tags: [rl, monte-carlo, control, exploration]
---

## Statement

Exploring Starts ensures all state-action pairs are visited by randomly starting episodes from (state, action) pairs. This eliminates the need for an ε-soft policy but requires restart capability.

### The problem, from first principles

Instead of using ε-soft exploration during episodes, start each episode from a random (s,a) pair and then follow the deterministic optimal policy. This guarantees coverage of all (s,a) without permanent exploration noise.

### From theory to code

Implement `mc_exploring_starts(env_step, num_episodes, gamma, seed=None)` which:
- Generates random start (state, action) pairs
- Simulates episode from that (s,a) under greedy policy
- Computes returns and updates Q
- Returns (Q, policy)

### Constraints

- Environment is deterministic or stochastic
- Start state can be any valid state
- Start action is sampled uniformly
- All (s,a) pairs must have nonzero probability of start
- Follow greedy policy after initial action

### Hints

<details>
<summary>Hint 1: Random initialization</summary>
Pick a state from {0, 1, ..., num_states-1} uniformly. Pick an action from {0, 1, ..., num_actions-1} uniformly.
</details>

<details>
<summary>Hint 2: Episode under greedy policy</summary>
Take initial action, then at each step choose greedy action from Q.
</details>

<details>
<summary>Hint 3: First-visit update</summary>
Update Q for first occurrence of each (s,a) in episode.
</details>

## Theory

### The simple version

Start each episode at a random (state, action) pair. Then follow the deterministic greedy policy. Average returns for each (s,a). This guarantees exploration without ε.

### The algorithm

1. Initialize Q(s,a) and π(s) = argmax Q(s,a)
2. For each episode:
   a. Pick random (s,a) as start
   b. Take action a, then follow π for rest of episode
   c. Update Q with returns from first visit
3. After each episode, update π(s) = argmax Q(s,a)

### Exploring Starts vs Epsilon-Soft

Exploring Starts: no exploration noise in the policy, but requires ability to start from any (s,a).
Epsilon-Soft: policy is always ε-exploratory, works in any MDP without restart.

### Convergence

Exploring Starts MC converges to π* (the optimal policy) almost surely, with no approximation error from exploration.

## Explanation

Exploring Starts is elegant in theory: by guaranteeing coverage, you avoid the bias of ε-soft policies. In practice, it requires environment control (ability to reset to arbitrary states), which is unrealistic for many problems. But it's a clean theoretical result and works well in simulation.
