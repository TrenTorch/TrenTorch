---
title: RBF Feature Approximation
name: rl-rbf-features
difficulty: Advanced
tags: [rl, rbf, function-approximation, kernels]
---

## Statement

RBF (Radial Basis Function) features: nonlinear features using Gaussian kernels. Each feature is exp(-||s - center||^2 / (2σ^2)).

### The problem, from first principles

Linear features can't capture nonlinearities. RBFs place Gaussian bumps at fixed centers, allowing nonlinear function approximation while keeping learning linear in parameters.

### From theory to code

Implement `rbf_features(state, centers, sigma)` which:

- Takes a state and set of Gaussian centers
- Computes distance from state to each center
- Returns exp(-distance^2 / (2 * sigma^2)) for each center
- Output shape: (num_centers,)

### Constraints

- Centers typically placed on grid or randomly in state space
- σ controls width of Gaussian
- Linear layer on top of RBF features

### Hints

<details>
<summary>Hint 1: Distance computation</summary>
Use Euclidean distance: sqrt((s - c)^T (s - c))
</details>

<details>
<summary>Hint 2: Gaussian kernel</summary>
exp(-||difference||^2 / (2*sigma^2))
</details>

<details>
<summary>Hint 3: Vectorized computation</summary>
Use np.linalg.norm for batch distances
</details>

## Theory

### RBF basis functions

Each basis function φ_i(s) = exp(-||s - c_i||^2 / (2σ^2))

Value function: V(s) = Σ w_i φ_i(s)

### Expressiveness

Can approximate smooth functions arbitrarily well with enough RBFs (universal approximator).

## Explanation

RBFs are classical nonlinear basis for RL. Replaced by neural networks but still useful for interpretability.
