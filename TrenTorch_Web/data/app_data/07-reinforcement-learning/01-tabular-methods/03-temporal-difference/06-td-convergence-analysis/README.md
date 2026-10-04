---
title: TD Convergence Analysis
name: rl-td-convergence-analysis
difficulty: Intermediate
tags: [rl, temporal-difference, convergence, analysis]
---

## Statement

Analyze TD(0) convergence on a simple environment: track how V estimates converge to true values as episodes increase.

### The problem, from first principles

TD learns online by bootstrapping. Does it converge? How fast? This question asks you to implement TD(0) and measure convergence rate, comparing to known ground truth values.

### From theory to code

Implement `td_convergence_analysis(episodes, true_values, gamma, alpha)` which:
- Takes episodes (list of (state, reward, next_state) tuples)
- Takes dict of true_values {state: true_value}
- Runs TD(0) with given gamma and alpha
- Returns (V_estimates, mse_per_episode) where MSE is mean squared error vs true values

### Constraints

- episodes are a list of complete episode sequences
- true_values is ground truth for comparison
- alpha is learning rate
- Return both final estimates and MSE trajectory

### Hints

<details>
<summary>Hint 1: Run TD incrementally</summary>
Process episodes one by one, tracking MSE after each.
</details>

<details>
<summary>Hint 2: Compute MSE</summary>
For each state visited, compute (V_estimate - true_value)^2 and average.
</details>

<details>
<summary>Hint 3: Track convergence</summary>
Record MSE after each episode in a list.
</details>

## Theory

### The simple version

Run TD on episodes from a known environment. After each episode, compute how close your V estimates are to the true values. Watch MSE decrease over time.

### Convergence guarantee

Under standard conditions (decreasing α, sufficient visits), TD(0) converges to V^π almost surely.

### TD vs MC vs DP

TD: online, model-free, bootstraps (can converge before episode ends)
MC: offline, model-free, no bootstrap (wait for episode end)
DP: online, requires model, bootstrap from model

### Learning rate effects

Large α: fast initial learning, high variance, possible divergence
Small α: slow learning, stable convergence
Decreasing α: convergence guarantee

## Explanation

This question combines theory (convergence) and practice (empirical measurement). It shows that despite bootstrapping's bias, TD converges to the right answer.
