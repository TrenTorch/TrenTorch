---
title: Feature Engineering for RL
name: rl-feature-engineering
difficulty: Intermediate
tags: [rl, features, approximation, preprocessing]
---

## Statement

Good features are critical for function approximation. Design features that capture relevant state dimensions while remaining normalized and sparse.

### The problem, from first principles

Linear approximation V(s) = w^T φ(s) is only as good as features φ(s). Raw pixels are useless; game state position, velocity, health matter. Feature engineering bridges raw states and learnable representations.

### From theory to code

Implement `polynomial_features(state, degree)` which:
- Takes state (scalar or vector)
- Returns polynomial feature expansion: [1, s, s^2, ..., s^d]
- Normalizes features to zero mean, unit variance

### Constraints

- Handles scalar or 1D array input
- Degree >= 1
- Normalize using running mean/std
- Return normalized feature vector

### Hints

<details>
<summary>Hint 1: Polynomial basis</summary>
[1, x, x^2, x^3, ...] for degree d
</details>

<details>
<summary>Hint 2: Normalization</summary>
(φ - μ) / σ for each feature
</details>

<details>
<summary>Hint 3: RBF features</summary>
Radial basis: exp(-||s - c_i||^2 / σ^2) for centers c_i
</details>

## Theory

### The simple version

Transform raw state into features that better capture value differences. Polynomials, RBF, tile coding all work.

### Common feature types

1. **Polynomial**: [1, s, s^2, ...]
2. **RBF**: exp(-(s-c)^2/σ^2)
3. **Tile coding**: binary grid representation
4. **Hand-crafted**: domain knowledge

### Feature scaling

Critical: normalize features to zero mean, unit variance. Prevents weight divergence.

## Explanation

Feature engineering is an art. Good features reduce approximation error dramatically. Deep RL skips this by learning features (via neural networks), but understanding manual features helps interpret learned representations.
