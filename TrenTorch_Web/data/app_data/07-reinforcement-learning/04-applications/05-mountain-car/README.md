---
title: Mountain Car Environment
name: rl-mountain-car
difficulty: Intermediate
tags: [rl, mountain-car, exploration, sparse-reward]
---

## Statement

Mountain Car: push car up a one-dimensional mountain. State: [position, velocity]. Actions: [left, neutral, right]. Reward: -1 per step, +10 at goal. Hard exploration problem.

### The problem, from first principles

Car can't accelerate enough to go straight up. Must oscillate back and forth to gain momentum. Sparse rewards force exploration and backward chaining.

### From theory to code

Implement `simulate_mountain_car(initial_state, actions, max_steps)` which:
- Position in [-1.2, 0.6], velocity in [-0.07, 0.07]
- Actions: apply -1, 0, or +1 force
- Reward: -1 per step unless at goal (x >= 0.5)
- Returns trajectory with state and rewards

### Constraints

- Gravity = 0.0025
- Friction = 0.01
- Bounds clipping at [-1.2, 0.6]
- Episode terminates at goal or max_steps

### Hints

<details>
<summary>Hint 1: Oscillation needed</summary>
Can't climb mountain directly, must swing back and forth
</details>

<details>
<summary>Hint 2: Physics simple</summary>
v += (action - gravity - friction*v) * dt
</details>

<details>
<summary>Hint 3: Exploration critical</summary>
Sparse rewards make exploration essential
</details>

## Theory

### Mountain Car MDP

Classic benchmark with negative rewards only until goal.
Forces algorithms to explore optimally due to sparse feedback.

## Explanation

Mountain Car tests exploration. Good exploration = 200-step solution, bad = 10000+ steps.
