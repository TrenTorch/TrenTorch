---
title: Imitation Learning from Demonstrations
name: rl-imitation-learning
difficulty: Advanced
tags: [rl, imitation, demonstrations, behavioral-cloning]
---

## Statement

Learn from expert demonstrations: train policy to mimic expert behavior using supervised learning on (state, action) pairs.

### The problem, from first principles

RL exploration is expensive. If expert demonstrations available, learn directly by supervised learning. Behavioral cloning minimizes cross-entropy loss on expert actions.

### From theory to code

Implement `behavioral_cloning_loss(policy_logits, expert_actions)` which:
- Takes predicted action logits and expert action labels
- Computes cross-entropy loss between policy and expert
- Averages over batch
- Returns scalar loss

### Constraints

- Expert dataset can be small but must be representative
- Distribution mismatch: learned policy diverges from expert
- Requires expert demonstrations (offline)

### Hints

<details>
<summary>Hint 1: Supervised learning</summary>
Treat as action classification: cross-entropy between predicted and expert action
</details>

<details>
<summary>Hint 2: Logits to probability</summary>
Use log_softmax for numerical stability
</details>

<details>
<summary>Hint 3: Distribution mismatch</summary>
Policy must handle states outside expert's distribution (DAgger addresses this)
</details>

## Theory

### Behavioral cloning

Minimize: L = -E[log π(a_expert | s)]

Direct supervised learning of expert policy.

### Issues

Distribution mismatch: expert training data covers different state distribution than policy's execution traces.

## Explanation

Imitation learning jumpstarts learning, but needs RL for optimality. Modern approaches combine both.
