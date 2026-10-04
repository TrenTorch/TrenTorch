---
title: Expected SARSA
name: rl-expected-sarsa
difficulty: Intermediate
tags: [rl, temporal-difference, control, on-policy]
---

## Statement

Expected SARSA is like SARSA but replaces the sampled next action with the expected value over the policy. It's safer and lower-variance than standard SARSA.

### The problem, from first principles

SARSA updates with the next action a', which can be unlucky (negative reward due to exploration). Expected SARSA averages over the policy: E_π[Q(s',a)] = Σ_a π(a|s')Q(s',a).

### From theory to code

Implement `expected_sarsa(env_step, num_episodes, epsilon, gamma, alpha, seed=None)` which:
- Generates episodes under ε-greedy policy
- Updates Q(s,a) using: Q(s,a) = Q(s,a) + α[r + γE_π[Q(s',a)] - Q(s,a)]
- Returns (Q, policy)

### Constraints

- Calculate expected Q value under ε-greedy policy
- E[Q(s',a)] = (1-ε)*max Q(s',a) + (ε/|A|)*Σ_a Q(s',a)
- Update online
- Return final Q and policy

### Hints

<details>
<summary>Hint 1: Expected value formula</summary>
E[Q(s',a)] = (1-ε)*argmax + (ε/|A|)*sum_of_all
</details>

<details>
<summary>Hint 2: Compute expectation</summary>
For each state, compute weighted average of Q values under ε-soft policy.
</details>

<details>
<summary>Hint 3: Update Q</summary>
Use the expected Q value instead of a sampled action's value.
</details>

## Theory

### The simple version

At each step, instead of using the Q value of the next action you take, use the average Q value under your current policy.

### The formula

Q(s,a) := Q(s,a) + α[r + γ E_π[Q(s',a)] - Q(s,a)]

where E_π[Q(s',a)] = (1-ε)max_a Q(s',a) + (ε/|A|)Σ_a Q(s',a)

### Expected SARSA properties

- On-policy: learns about the policy being followed
- Lower variance than SARSA: uses expectation, not a sample
- Safer: less affected by unlucky exploration
- Converges slower than Q-learning: must explore

## Explanation

Expected SARSA bridges SARSA and Q-learning: it explores safely like SARSA but with lower variance by averaging over the policy. Good when you want exploration guarantees without Q-learning's off-policy bias.
