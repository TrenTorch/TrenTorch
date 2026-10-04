---
title: Dueling Network Architectures
name: rl-dueling-networks
difficulty: Advanced
tags: [rl, dueling, architecture, value-advantage]
---

## Statement

Dueling networks: separate value V(s) and advantage A(s,a) streams, recombine as Q(s,a) = V(s) + A(s,a) - mean_a A(s,a).

### The problem, from first principles

Value and advantage are learned jointly in standard Q-networks, causing instability. Dueling architectures separate the learning: value stream learns state goodness, advantage stream learns action differentiation.

### From theory to code

Implement `dueling_q_values(state, value_stream, advantage_stream)` which:
- Takes separate value and advantage network outputs
- Combines via: Q = V + (A - mean(A))
- Mean-advantage subtraction stabilizes training
- Returns Q-values for all actions

### Constraints

- Both streams process same state features
- Advantage centering reduces variance
- Maintains expressiveness of Q-learning

### Hints

<details>
<summary>Hint 1: Separate streams</summary>
Value network outputs scalar V(s), advantage outputs vector A(s,a)
</details>

<details>
<summary>Hint 2: Combination formula</summary>
Q = V + (A - mean_a A), not just V + A
</details>

<details>
<summary>Hint 3: Stabilization</summary>
Mean centering reduces learning instability without reducing Q expressiveness
</details>

## Theory

### Dueling architecture

Network splits into two streams before output layer:
- Value stream: state -> ... -> V(s) (scalar)
- Advantage stream: state -> ... -> A(s,a) (vector of size |A|)

Reconstruction: Q(s,a) = V(s) + A(s,a) - E_a[A(s,a)]

### Advantage

Value and advantage learn complementary representations. Much faster than standard DQN.

## Explanation

Dueling networks are standard in modern DQN variants. Simple trick, big impact on learning speed and stability.
