---
title: Monte Carlo Control Simulation
name: rl-monte-carlo-control-sim
difficulty: Intermediate
tags: [rl, monte-carlo, control, simulation]
---

## Statement

Build an end-to-end MC control system that learns a policy on a simple gridworld environment. Generate episodes, update Q values, and track convergence.

### The problem, from first principles

You have a simple environment. Run MC control: collect episodes under ε-soft policy, estimate Q values, improve the policy. Track how Q converges and how the policy evolves.

### From theory to code

Implement `mc_control_gridworld(num_episodes, epsilon, gamma)` which:
- Runs a simple gridworld: 4x4 grid, 4 actions (N, S, E, W)
- Start at (0,0), goal at (3,3), each step reward -1, goal reward +10
- Runs MC control for num_episodes
- Returns (Q_final, policy, rewards_per_episode)

### Constraints

- Gridworld is 4x4, state = (row, col)
- Actions: 0=North, 1=South, 2=East, 3=West
- Collision with boundary: stay in place
- Episode ends when reaching (3,3) or after 50 steps
- Update Q after each episode

### Hints

<details>
<summary>Hint 1: Define the environment</summary>
Implement step(state, action) that returns (next_state, reward, done).
</details>

<details>
<summary>Hint 2: Collect episodes</summary>
Generate episodes using ε-soft policy: explore with prob ε, exploit with prob 1-ε.
</details>

<details>
<summary>Hint 3: Update Q</summary>
After each episode, compute returns and average into Q values.
</details>

## Theory

### The simple version

Run a RL agent on a gridworld for 100 episodes. Watch Q values and the learned policy converge toward the optimal path to the goal.

### The algorithm

1. Initialize Q(s,a) and ε-soft π
2. For each episode:
   a. Start at (0,0)
   b. Take actions under ε-soft policy until goal or timeout
   c. Compute returns
   d. Update Q by averaging returns
3. Track episode lengths and cumulative reward

### Convergence criteria

MC control converges when:
- Q values stabilize (change < threshold)
- Policy stabilizes (same actions chosen)
- Episode reward increases toward optimal

## Explanation

This capstone integrates prediction (value estimation) and control (policy improvement) into a single working system. The gridworld is small enough to verify by hand, but large enough to show learning dynamics.
