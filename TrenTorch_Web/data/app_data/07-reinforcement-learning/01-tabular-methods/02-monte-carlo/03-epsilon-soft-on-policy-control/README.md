---
title: Epsilon-Soft On-Policy Monte Carlo Control
name: rl-epsilon-soft-mc-control
difficulty: Intermediate
tags: [rl, monte-carlo, control, on-policy]
---

## Statement

Epsilon-Soft Monte Carlo Control learns an optimal policy by alternating between evaluation (averaging returns) and improvement (shifting toward greedy actions with probability 1-ε).

### The problem, from first principles

Given a non-stationary policy that is ε-soft (probability ≥ ε/|A| for every action), estimate Q^π(s,a) and improve π by shifting weight toward best actions. Unlike bandits, we must balance exploration (epsilon) with exploitation (greedy).

### From theory to code

Implement `epsilon_soft_mc_control(env_step, num_episodes, epsilon, gamma)` which:
- Runs `num_episodes` episodes where at each state, we take action with probability (1-ε) if best, else uniform random among remaining
- Tracks Q values (state-action pair returns)
- Tracks action counts
- Returns (Q_final, policy_final) where policy[s] is the best action

The env_step function has signature: env_step(state, action) -> (next_state, reward, done)

### Constraints

- epsilon in (0, 1)
- ε-soft policy: always explores, but biased toward greedy
- Update Q incrementally or batch-average
- Return final Q dict and greedy policy dict

### Hints

<details>
<summary>Hint 1: Track Q and counts</summary>
Store Q values and visit counts per (state, action) pair.
</details>

<details>
<summary>Hint 2: Generate episodes</summary>
Sample actions epsilon-soft: with prob 1-ε choose argmax Q[s], else uniform random.
</details>

<details>
<summary>Hint 3: Update Q</summary>
After each episode, average returns for first (or every) visit to each (s,a).
</details>

## Theory

### The simple version

Run policy for many episodes. Track (state, action) returns. Every 10 episodes, improve policy toward greedy w.r.t. Q.

### The algorithm

1. Initialize Q(s,a) arbitrarily, ε-soft policy π
2. Loop:
   a. Generate episode under π
   b. For each (s,a) in episode, average the return into Q
   c. For each s: π(s,a) = (1-ε)/|A(s)| + (argmax Q / |A(s)|) * ε (or 1-ε for greedy)

### On-policy vs Off-policy

On-policy: learn π while following π (ε-soft ensures exploration).
Off-policy: learn π* while following a different policy (requires importance sampling).

Epsilon-soft is on-policy: the exploration in the learned policy matches the exploration in data collection.

### Convergence

Epsilon-soft MC converges to π_ε*, the best ε-soft policy (not the optimal policy, due to exploration).

## Explanation

Epsilon-soft control is the simplest control algorithm: keep π slightly exploratory and greedily improve Q. The cost: you never reach the truly optimal policy, but exploration is guaranteed.
