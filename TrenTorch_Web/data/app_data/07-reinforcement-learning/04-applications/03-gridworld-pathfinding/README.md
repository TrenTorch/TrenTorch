---
title: Gridworld Pathfinding
name: rl-gridworld-pathfinding
difficulty: Intermediate
tags: [rl, gridworld, pathfinding, mdp]
---

## Statement

Gridworld: agent navigates NxN grid from start to goal. Actions: [up, down, left, right]. Reward: -1 per step, +10 at goal. Walls block movement.

### The problem, from first principles

Simple environment to test RL algorithms. Finite state/action spaces, deterministic dynamics, sparse rewards. Optimal policy finds shortest path.

### From theory to code

Implement `solve_gridworld(grid, start, goal, max_steps=1000)` which:

- Uses value iteration or Q-learning
- grid: 2D array where 1=wall, 0=free
- Returns optimal policy as NxN array of actions
- Policy guides agent from any state to goal

### Constraints

- 4 actions: up(0), down(1), left(2), right(3)
- Agent stays in place if action hits wall
- Deterministic transitions
- Goal is absorbing state

### Hints

<details>
<summary>Hint 1: Value iteration</summary>
V(s) = max_a [R(s,a) + γ V(s')]
</details>

<details>
<summary>Hint 2: Policy extraction</summary>
π(s) = argmax_a [R(s,a) + γ V(s')]
</details>

<details>
<summary>Hint 3: Boundary handling</summary>
Out-of-bounds actions keep agent in place
</details>

## Theory

### Gridworld MDP

States: grid cells
Actions: 4 cardinal directions
Transitions: deterministic movement (blocked by walls)
Rewards: -1 per step, +10 at goal

### Value Iteration

Iteratively apply Bellman update until convergence.

## Explanation

Gridworld is the canonical testbed for tabular RL. Every RL textbook covers it.
