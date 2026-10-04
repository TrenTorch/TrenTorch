---
title: TD(0) Prediction
name: rl-td-prediction
difficulty: Intermediate
tags: [rl, temporal-difference, td-learning, prediction]
---

## Statement

Temporal Difference (TD) learning combines ideas from MC and DP: update value estimates using a mix of immediate reward and bootstrapped next-state value. TD(0) is the one-step version.

### The problem, from first principles

Instead of waiting for episode completion (MC) or needing the full model (DP), TD updates immediately: V(s) = V(s) + α[r + γV(s') - V(s)]. The term [r + γV(s') - V(s)] is the TD error.

### From theory to code

Implement `td_prediction(episodes, gamma, alpha)` which:

- Takes episodes as list of (state, reward, next_state) tuples
- Takes discount factor γ and step size α
- Returns dict {state: estimated_value}

Update values incrementally using TD(0) rule.

### Constraints

- alpha in (0, 1], typically 0.1
- Process episode transitions online
- Terminal states have value 0
- Update only visited states

### Hints

<details>
<summary>Hint 1: Process online</summary>
For each (s, r, s') in episode, update V(s) immediately.
</details>

<details>
<summary>Hint 2: Compute TD error</summary>
delta = r + gamma * V(s') - V(s)
</details>

<details>
<summary>Hint 3: Update V</summary>
V(s) = V(s) + alpha * delta
</details>

## Theory

### The simple version

Walk through an episode. At each step, update the current state's value using the immediate reward and the next state's current estimate.

### The formula

V(s) := V(s) + α[r + γV(s') - V(s)]

where α is the learning rate and [r + γV(s') - V(s)] is the TD error.

### TD vs MC vs DP

MC: V(s) = V(s) + α[G_t - V(s)], no bootstrapping
TD: V(s) = V(s) + α[r + γV(s') - V(s)], one-step bootstrapping
DP: V(s) = E[r + γV(s')]

TD is online (update immediately), model-free (no model needed), and can learn from incomplete episodes.

## Explanation

TD learning is the foundation of modern RL. By bootstrapping (using current estimates), TD has lower variance than MC but may have bias from function approximation errors.
