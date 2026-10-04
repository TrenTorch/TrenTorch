---
title: Linear Function Approximation
name: rl-linear-approx
difficulty: Intermediate
tags: [rl, function-approximation, linear, approximation]
---

## Statement

Linear function approximation represents state values as a linear combination of features: V(s) = w^T * φ(s), where φ(s) is a feature vector and w are weights.

### The problem, from first principles

Tabular methods scale to 10^6 states but fail at 10^9 states or continuous spaces. Function approximation generalizes: learn weights w such that V(s) = w^T * φ(s) approximates the true value for all states.

### From theory to code

Implement `linear_td_update(w, phi, reward, next_phi, gamma, alpha)` which:
- Takes weights w and feature vectors phi(s), phi(s')
- Takes reward and discount factor
- Updates weights using TD: w := w + α[r + γw^T*φ(s') - w^T*φ(s)] * φ(s)
- Returns updated w

### Constraints

- phi vectors are numpy arrays
- w is weight vector (same size as phi)
- alpha is learning rate
- Return updated w

### Hints

<details>
<summary>Hint 1: TD error</summary>
delta = r + gamma * w^T * phi_next - w^T * phi
</details>

<details>
<summary>Hint 2: Gradient</summary>
w := w + alpha * delta * phi
</details>

<details>
<summary>Hint 3: Feature scaling</summary>
Normalize features to mean 0, variance 1 for stability.
</details>

## Theory

### The simple version

Instead of one value per state, learn a weight vector w. Value of state s is dot product: w · features(s).

### The formula

V(s) = w^T φ(s)
w := w + α[r + γV(s') - V(s)] * φ(s)

### Feature design

Linear approximation only works if features are good. Good features:
- Capture relevant state dimensions
- Are normalized
- Cover the state space

### Convergence

Linear TD converges to minimum of expected TD error (under decreasing α).

## Explanation

Linear approximation is the bridge from tabular to deep RL. It's stable, interpretable, and much more efficient than tabular for large state spaces.
