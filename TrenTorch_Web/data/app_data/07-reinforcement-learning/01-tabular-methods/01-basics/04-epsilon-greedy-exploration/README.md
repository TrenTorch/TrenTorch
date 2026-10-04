---
title: Epsilon-Greedy Action Selection for n-Armed Bandit
name: rl-epsilon-greedy-exploration
difficulty: Beginner
tags: [rl, bandits, exploration, exploration-exploitation]
---

## Statement

Epsilon-greedy is the simplest exploration strategy: with probability ε, pick a random action; with probability 1-ε, pick the greedy action (highest estimated value).

### The problem, from first principles

The exploration-exploitation trade-off is central to reinforcement learning:

- **Exploit**: choose the action with the highest estimated value (greedy)
- **Explore**: try other actions to learn better estimates

Epsilon-greedy balances them: most of the time (1-ε), you exploit; occasionally (ε), you explore randomly. This ensures:

- You eventually find the optimal action (exploration)
- You spend most time on good actions (exploitation)

### From theory to code

Implement `select_epsilon_greedy_action(q_values, epsilon, rng)` which:

- Takes action values Q(a) for all actions a (1D array or list)
- Takes epsilon ∈ [0, 1]
- Takes a numpy random number generator
- Returns the selected action index (int)

With probability ε, return a random action index. With probability 1-ε, return the index of the highest-valued action.

### Constraints

- q_values has at least 1 action
- epsilon is in [0, 1]
- rng is a numpy random generator (use `rng.random()` for uniform [0,1) and `rng.choice()` for random selection)
- If there are ties for max, break ties deterministically or randomly (either is fine)

### Hints

<details>
<summary>Hint 1: Random vs Greedy</summary>
Generate u = rng.random(). If u < epsilon, choose random. Else choose greedy.
</details>

<details>
<summary>Hint 2: Greedy action</summary>
Use np.argmax(q_values) to find the highest-valued action.
</details>

<details>
<summary>Hint 3: Random action</summary>
Use rng.choice(len(q_values)) or rng.integers(0, len(q_values)).
</details>

## Theory

### The simple version

10 actions with values [1, 2, 5, 3, ...]. With ε=0.1:

- 90% of the time: pick action 2 (value=5)
- 10% of the time: pick a uniformly random action (including the optimal one)

Over time, you lock in on the best action, but occasionally try others to verify they're still worst.

### The formula

P(a_t = a) = ε/|A| + (1 - ε) · 1[a = argmax Q(a)]

For the greedy action a*, P(a_t = a*) = ε/|A| + (1 - ε).
For any other action, P(a_t = a) = ε/|A|.

### Why it works

If ε > 0, every action has nonzero probability, so you'll eventually sample all actions infinitely often (with probability 1). This guarantees you discover the true best action. Meanwhile, 1-ε ≥ 0 means you exploit what you've learned, keeping regret low.

### Convergence

With constant ε, the algorithm converges to ε-optimal: the regret per step approaches ε·(best - average action value). Decreasing ε over time lets you explore heavily early and exploit later.

## Explanation

Epsilon-greedy is perhaps the most widely used exploration strategy because it's:

1. **Simple**: one hyperparameter (ε)
2. **Effective**: provably optimal in bandit theory
3. **Flexible**: ε can be constant, or decay over time, or adapted per state

In practice, ε ∈ [0.01, 0.1] works well for most problems.
