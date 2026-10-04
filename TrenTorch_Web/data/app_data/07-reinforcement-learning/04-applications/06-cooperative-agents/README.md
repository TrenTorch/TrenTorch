---
title: Cooperative Multi-Agent RL
name: rl-cooperative-agents
difficulty: Advanced
tags: [rl, multi-agent, cooperation, communication]
---

## Statement

Multi-agent RL: N agents cooperate to maximize shared reward. Each agent observes partial state, must coordinate via learned behavior or communication.

### The problem, from first principles

Multiple agents learning simultaneously create non-stationary environment. Agents must learn to cooperate despite seeing only partial observations. Scalability challenge.

### From theory to code

Implement `compute_cooperative_value(individual_values, reward_scale)` which:

- Takes individual agent value estimates
- Combines into cooperative objective
- Values shared reward: combined_value = sum(individual_values) + reward_scale * shared_reward
- Returns total cooperative value

### Constraints

- Partial observability: each agent sees subset of state
- Non-stationary: other agents' policies changing
- Scalability: learning degrades with more agents
- Communication may help but adds complexity

### Hints

<details>
<summary>Hint 1: Shared reward</summary>
All agents get same reward signal for cooperative success
</details>

<details>
<summary>Hint 2: Credit assignment</summary>
Difficult to assign credit: which agent caused success?
</details>

<details>
<summary>Hint 3: QMIX/MADDPG</summary>
Modern approaches: value decomposition or centralized training
</details>

## Theory

### Cooperative multi-agent

Shared reward: R = f(joint_action)
Each agent learns independently but receives same reward.

Challenge: credit assignment - which agent's action contributed?

## Explanation

Multi-agent RL is hot: self-play (AlphaGo), human-AI cooperation, swarms. Hard unsolved problem.
