---
title: First-Visit Monte Carlo Prediction
name: rl-first-visit-mc-prediction
difficulty: Intermediate
tags: [rl, monte-carlo, value-estimation, prediction]
---

## Statement

First-Visit Monte Carlo prediction estimates the value of a state by averaging returns from episodes, counting only the first visit to that state in each episode.

### The problem, from first principles

Given episodes (trajectories) from a fixed policy π, estimate V^π(s) for each state s. Unlike bootstrapping, MC uses full episode returns without a model. The "first-visit" constraint ensures independence: each episode contributes at most one return for state s.

### From theory to code

Implement `estimate_state_values(episodes, gamma)` which:

- Takes a list of episodes (each is a list of (state, reward) tuples)
- Takes discount factor γ
- Returns a dict {state: estimated_value}

Use first-visit semantics and unbiased averaging.

### Constraints

- Each episode is a list of (state, reward) pairs
- Only count the first visit to each state per episode
- Return a dict mapping states to float values
- If a state never appears, it doesn't appear in the dict (or value 0.0)

### Hints

<details>
<summary>Hint 1: Track visits</summary>
For each state, keep a list of returns from first visits. Average them at the end.
</details>

<details>
<summary>Hint 2: First-visit check</summary>
For each episode, iterate through states seen and mark first visits.
</details>

<details>
<summary>Hint 3: Compute return</summary>
For each first visit at index i, sum future rewards with discounts.
</details>

## Theory

### The simple version

Run policy π for 3 episodes. Track returns from first visits to each state. Average them.

### The formula

V(s) = (1/n) Σ_i G_i(s)

where G_i(s) is the return from the first visit to s in episode i, and n is the count of episodes with a first visit to s.

### First-visit vs Every-visit

First-visit: includes return only from first occurrence.
Every-visit: includes all returns.

First-visit is unbiased; every-visit has lower variance but slight bias.

### Convergence

With infinite episodes, first-visit MC converges to the true V^π by law of large numbers.

## Explanation

Monte Carlo is model-free: you don't need environment dynamics. Run the policy, collect episodes, average returns. Simple, unbiased, but high variance (only one sample per episode per state).
