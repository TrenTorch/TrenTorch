---
title: SARSA (State-Action-Reward-State-Action)
name: rl-sarsa-control
difficulty: Intermediate
tags: [rl, temporal-difference, control, on-policy]
---

## Statement

SARSA is on-policy TD control: learn Q(s,a) using the tuple (s, a, r, s', a'). Like Qlearning but follows the behavior policy for the next action.

### The problem, from first principles

Update Q values online using observed transitions. Choose the next action under the current ε-soft policy, not the greedy policy. This makes it on-policy: learns about the policy being followed.

### From theory to code

Implement `sarsa(env_step, num_episodes, epsilon, gamma, alpha, seed=None)` which:

- Generates episodes under ε-greedy policy
- Updates Q(s,a) using: Q(s,a) = Q(s,a) + α[r + γQ(s',a') - Q(s,a)]
- Returns (Q, policy)

### Constraints

- epsilon in (0, 1)
- alpha in (0, 1], learning rate
- gamma in (0, 1], discount
- Update Q immediately after each transition
- Derive policy from Q

### Hints

<details>
<summary>Hint 1: Select actions epsilon-greedy</summary>
With prob 1-ε, pick argmax Q(s), else random action.
</details>

<details>
<summary>Hint 2: Observe transition</summary>
From (s,a), observe (r, s'), then select a' epsilon-greedy.
</details>

<details>
<summary>Hint 3: Update Q</summary>
Q(s,a) = Q(s,a) + α[r + γQ(s',a') - Q(s,a)]
</details>

## Theory

### The simple version

At each step, observe (s, a, r, s', a'). Update Q for (s,a) using the Q value of the next action a' (which you're about to take).

### The algorithm

1. Initialize Q(s,a)
2. For each episode:
   a. s = start, a = ε-greedy(s)
   b. Take a, observe (r, s')
   c. a' = ε-greedy(s')
   d. Q(s,a) := Q(s,a) + α[r + γQ(s',a') - Q(s,a)]
   e. s = s', a = a'
   f. Repeat until terminal

### On-policy vs Off-policy

SARSA: on-policy, updates Q for the policy being followed.
Qlearning: off-policy, updates Q for greedy policy.

SARSA explores safely (stays in ε-soft region), but never finds optimal policy (learns π_ε*).

## Explanation

SARSA is a workhorse of practical RL. It's safe (guarantees exploration) and simple, but converges to a suboptimal policy due to exploration noise.
