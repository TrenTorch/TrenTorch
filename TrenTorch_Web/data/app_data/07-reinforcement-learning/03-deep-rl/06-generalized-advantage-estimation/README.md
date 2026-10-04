---
title: Generalized Advantage Estimation (GAE)
name: rl-gae
difficulty: Advanced
tags: [rl, gae, advantage-estimation, variance-reduction]
---

## Statement

GAE: exponentially-weighted average of TD errors. Trades off variance (low λ) and bias (high λ) in advantage estimates.

### The problem, from first principles

TD(0) has low variance but high bias. MC has zero bias but high variance. GAE interpolates via λ: combines 1-step, 2-step, ..., n-step returns with exponential weights.

### From theory to code

Implement `gae(values, rewards, next_values, gamma, lambda_)` which:
- Computes TD residuals: δ = r + γV(s') - V(s)
- Exponentially weighted sum: A = Σ(γλ)^t δ_t
- Returns advantages array matching trajectory length

### Constraints

- λ in [0, 1]: low = variance, high = bias
- Typically λ = 0.95
- Must handle trajectory endings (done flags)

### Hints

<details>
<summary>Hint 1: TD residuals</summary>
δ_t = r_t + γV(s_{t+1}) - V(s_t)
</details>

<details>
<summary>Hint 2: Exponential weighting</summary>
gae_t = δ_t + (γλ) δ_{t+1} + (γλ)^2 δ_{t+2} + ...
</details>

<details>
<summary>Hint 3: Backward iteration</summary>
Compute from end of trajectory backward, accumulating exponentially
</details>

## Theory

### GAE algorithm

1. Compute TD residuals for entire trajectory
2. Backward pass: compute GAE advantage for each timestep
3. A_t = Σ_{l=0}^{∞} (γλ)^l δ_{t+l}

### Variance-Bias Tradeoff

λ=0: A = δ (one-step TD) = low variance, high bias
λ=1: A = sum of all future returns (MC) = zero bias, high variance
λ=0.95: sweet spot for most problems

## Explanation

GAE is the standard for modern policy gradient methods. Dramatically improves learning efficiency.
