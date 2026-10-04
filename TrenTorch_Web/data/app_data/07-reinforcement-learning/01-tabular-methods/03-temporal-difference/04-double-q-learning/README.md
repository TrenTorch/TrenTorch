---
title: Double Q-Learning
name: rl-double-q-learning
difficulty: Advanced
tags: [rl, temporal-difference, control, off-policy]
---

## Statement

Double Q-Learning addresses overestimation bias in standard Q-learning by maintaining two Q estimates and decoupling selection from evaluation.

### The problem, from first principles

Standard Q-learning uses max Q(s',a') which can overestimate values (max of noisy estimates is biased high). Double Q-learning uses one Q for selection and another for evaluation, reducing bias.

### From theory to code

Implement `double_q_learning(env_step, num_episodes, epsilon, gamma, alpha, seed=None)` which:
- Maintains two Q estimates: Q1 and Q2
- Updates both alternately
- Uses Q1 to select best action, Q2 to evaluate (and vice versa)
- Returns (Q_avg, policy)

### Constraints

- Two separate Q dictionaries
- Alternate which Q is used for selection vs evaluation
- Random choice of which Q to update each step
- Return averaged final Q values

### Hints

<details>
<summary>Hint 1: Two Q values</summary>
Keep Q1 and Q2 both as dicts.
</details>

<details>
<summary>Hint 2: Decoupling</summary>
Use one Q to pick best action, other Q to evaluate value.
</details>

<details>
<summary>Hint 3: Alternation</summary>
Each step, randomly choose which Q to update.
</details>

## Theory

### The simple version

Keep two separate Q estimates. To avoid overestimation, use one to find the best action and the other to estimate its value.

### The algorithm

1. Initialize Q1(s,a) and Q2(s,a)
2. For each step:
   a. a' = argmax Q1(s',a')
   b. Update Q2: Q2(s,a) := Q2(s,a) + α[r + γQ2(s',a') - Q(s,a)]
   c. Swap Q1 and Q2 roles (or randomly choose which to update)

### Why it works

max of noisy estimates is upward biased. By separating selection from evaluation, we get unbiased estimates.

### Convergence

Double Q-learning converges to Q* with lower bias and often faster convergence than standard Q-learning.

## Explanation

Double Q-learning is a simple but powerful fix to Q-learning's overestimation. In practice, it often produces better policies, especially in stochastic environments.
