---
name: k-armed-bandits-epsilon-greedy-action
title: Epsilon-greedy action selection
tags: [reinforcement-learning, bandits, exploration]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A bandit agent must keep trying the arm that looks best (exploitation) while occasionally trying others in case its estimates are wrong (exploration). Epsilon-greedy is the simplest rule: explore with a small fixed probability, otherwise exploit.

### From theory to code

Implement `epsilon_greedy_action(q_values, epsilon, rng)`. With probability `epsilon` return a uniformly random arm; otherwise return the arm with the highest estimated value.

### Constraints

- `q_values` is a one-dimensional array of current value estimates, one per arm.
- `rng` is a `numpy.random.Generator`; draw the explore/exploit decision from it with `rng.random()`, and the random arm with `rng.integers(...)`.
- On exploiting, break ties toward the lowest arm index.
- Return a Python `int`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Draw one number in `[0, 1)`; if it is below `epsilon`, explore.

</details>

<details><summary>Hint 2</summary>

`np.argmax` already returns the first maximum, which gives the required tie-break.

</details>

## Theory

### The simple version

With epsilon = 0.1 the agent exploits 90% of the time and picks a random arm 10% of the time. Epsilon = 0 never explores and can get stuck on a bad early favourite; epsilon = 1 never uses what it has learned.

### The formula

$$a = \begin{cases} \text{uniform random arm} & \text{with probability } \epsilon \\ \arg\max_a Q(a) & \text{with probability } 1 - \epsilon \end{cases}$$

### How libraries implement this

Gymnasium-style bandit and DQN code implements exactly this, usually with epsilon decayed over time.

## Explanation

Because the random draw happens first, epsilon = 0 never explores and epsilon = 1 always does. A random arm may coincide with the greedy one, so the greedy arm is chosen with probability `1 - epsilon + epsilon / k`.
