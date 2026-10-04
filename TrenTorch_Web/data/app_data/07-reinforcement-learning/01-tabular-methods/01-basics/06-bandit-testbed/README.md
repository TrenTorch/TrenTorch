---
title: Build a Multi-Armed Bandit Testbed
name: rl-bandit-testbed
difficulty: Intermediate
tags: [rl, bandits, experimentation, performance-evaluation]
---

## Statement

A bandit testbed is an experimental framework for evaluating bandit algorithms. You generate random bandit instances, run algorithms on them, and measure performance (cumulative regret, action accuracy).

### The problem, from first principles

To fairly compare epsilon-greedy and UCB, you need:

1. A random bandit instance (true rewards for each arm)
2. A way to run an algorithm on that instance
3. A way to measure performance (did we find the best arm?)

The testbed generates multiple independent bandits and averages the results across them. This controls for randomness in the problem and gives stable performance estimates.

### From theory to code

Build a class `BanditTestbed` with:

- Constructor: `__init__(num_arms, num_instances, seed)` - creates `num_instances` random bandits with `num_arms` arms
- Method: `run_algorithm(select_fn, num_steps)` - runs the selection function for `num_steps` steps on all instances
- Method: `get_results()` - returns (mean_rewards, optimal_counts, regrets)

True rewards are drawn from N(0, 1), then for each step, the agent selects an arm, observes a reward drawn from N(true_reward, 1).

### Constraints

- num_arms ≥ 2
- num_instances ≥ 1
- num_steps ≥ 1
- select_fn has signature: select_fn(q_estimates, counts, time_step, rng) -> action (int)
- Return three arrays: (rewards per step, times optimal arm was selected, cumulative regret)

### Hints

<details>
<summary>Hint 1: Class structure</summary>
Store the true arm rewards in __init__. In run_algorithm, track Q estimates, counts, and rewards for each instance.
</details>

<details>
<summary>Hint 2: Evaluation loop</summary>
For each step and each instance: select action, observe reward, update Q and counts, record result.
</details>

<details>
<summary>Hint 3: Results aggregation</summary>
Average rewards and regrets across instances. Count optimal selections across all instances.
</details>

## Theory

### The simple version

Create 100 bandits with 10 arms each. True rewards are random from N(0,1). Run epsilon-greedy for 1000 steps on each, average the results. Compare to UCB.

Metrics:

- **Regret**: sum of (best arm reward - selected arm reward)
- **Optimal %**: how often the best arm was chosen

### Experimental design

The testbed:

1. **Randomizes the problem**: each instance has different true rewards
2. **Averages across instances**: results are stable and unbiased
3. **Isolates the algorithm**: the only variable is the selection function

This is the standard way in bandit papers to evaluate algorithms.

### Why testbeds matter

Bandits are stochastic. On a single run, luck can dominate. A testbed averages over luck, isolating algorithm quality.

## Explanation

Building testbeds is essential ML engineering. You're not just coding the algorithm; you're building the experimental apparatus to evaluate it fairly.

The key insight: separate the **problem instance** (true rewards) from the **algorithm** (selection function). This lets you test any algorithm by just changing the selection function while keeping the instances fixed.

In practice, bandit researchers use testbeds to benchmark new algorithms against baselines. You'll do the same here for epsilon-greedy, UCB, and others.
