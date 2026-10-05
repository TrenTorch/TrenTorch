---
title: Curiosity-Driven Exploration
name: rl-curiosity-driven
difficulty: Advanced
tags: [rl, exploration, intrinsic-motivation, curiosity]
---

## Statement

Curiosity-driven exploration: reward model predicts next state from (s, a). Prediction error is intrinsic reward. High error = high curiosity.

### The problem, from first principles

Extrinsic rewards can be sparse. Agent explores due to curiosity: trying actions that lead to unpredictable next states. Intrinsic reward = prediction error.

### From theory to code

Implement `curiosity_reward(state, action, next_state, predictor, curiosity_strength)` which:

- Predictor network maps (s,a) -> s_predicted
- Intrinsic reward: ||s_next - s_predicted||^2
- Scales reward by curiosity_strength
- Returns combined reward

### Constraints

- Prediction error only on state features (not actions)
- Need to avoid reward hacking (learning trivial random dynamics)
- Usually combined with extrinsic rewards

### Hints

<details>
<summary>Hint 1: Forward model</summary>
Predictor outputs predicted next state
</details>

<details>
<summary>Hint 2: Prediction error</summary>
L2 distance between predicted and actual next state
</details>

<details>
<summary>Hint 3: Novelty bonus</summary>
Higher error = more novel = higher curiosity reward
</details>

## Theory

### ICM (Intrinsic Curiosity Module)

Forward model learns to predict next state from (s, a).
Prediction error is intrinsic motivation signal.

Intrinsic reward r_i = β || φ(s_t+1) - f(φ(s_t), a_t) ||^2

### Exploration-Exploitation

Curiosity provides exploration bonus without hand-crafted shaping.

## Explanation

Curiosity is powerful for sparse-reward environments. Powers many state-of-the-art exploration algorithms.
