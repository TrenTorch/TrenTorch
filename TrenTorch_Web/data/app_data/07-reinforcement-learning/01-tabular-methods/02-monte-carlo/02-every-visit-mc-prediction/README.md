---
title: Every-Visit Monte Carlo Prediction
name: rl-every-visit-mc-prediction
difficulty: Intermediate
tags: [rl, monte-carlo, value-estimation, prediction]
---

## Statement

Every-Visit Monte Carlo is a variant of MC prediction that averages returns from all visits to a state, not just the first. This introduces a slight bias but can reduce variance in some settings.

### The problem, from first principles

Given episodes from a fixed policy π, estimate V^π(s) using every occurrence of state s in each episode. Unlike first-visit, a state visited multiple times in one episode contributes multiple returns.

### From theory to code

Implement `estimate_state_values_every_visit(episodes, gamma)` which:
- Takes a list of episodes (each is a list of (state, reward) tuples)
- Takes discount factor γ
- Returns a dict {state: estimated_value}

Use every-visit semantics and unbiased averaging.

### Constraints

- Count all visits to each state, including repeats within an episode
- Compute return from each visit onward
- Return a dict mapping states to float values
- If a state never appears, exclude it from the dict

### Hints

<details>
<summary>Hint 1: No first-visit check</summary>
Unlike first-visit MC, don't track visited_states. Just iterate through all positions.
</details>

<details>
<summary>Hint 2: Accumulate returns</summary>
For each index i in the episode, compute the discounted return from i onward.
</details>

<details>
<summary>Hint 3: Average all returns</summary>
Each state gets all its returns averaged, regardless of how many times it appeared.
</details>

## Theory

### The simple version

Run policy π. For each state, record ALL returns from all visits. Average them.

### The formula

V(s) = (1/n) Σ_i G_i(s)

where G_i(s) is the return from the i-th visit to s (including repeats), and n is the total count of visits (including repeats).

### First-visit vs Every-visit

First-visit: one return per episode per state. Unbiased, higher variance.
Every-visit: all returns per episode per state. Slightly biased, lower variance.

In the limit, both converge to V^π(s).

### Convergence

Every-visit MC converges to V^π(s) almost surely, though with a slight bias that vanishes as sample size grows.

## Explanation

Every-visit exploits repeated visits to the same state within an episode. If a state appears 3 times, you get 3 data points. This can speed up convergence in some problems but trades unbiasedness for variance reduction.
