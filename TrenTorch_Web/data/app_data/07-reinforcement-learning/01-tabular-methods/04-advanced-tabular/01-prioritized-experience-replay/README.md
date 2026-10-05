---
title: Prioritized Experience Replay
name: rl-prioritized-experience-replay
difficulty: Advanced
tags: [rl, experience-replay, importance-sampling, optimization]
---

## Statement

Prioritized Experience Replay (PER) samples high-TD-error transitions more often during learning, focusing effort on surprising/informative experiences.

### The problem, from first principles

Standard experience replay samples uniformly. But some transitions are more informative: high TD-error means the value estimate is wrong. PER uses a priority weight proportional to |TD-error| to oversample these transitions.

### From theory to code

Implement `prioritized_replay_buffer(transitions, td_errors, batch_size, alpha=0.6)` which:

- Takes transitions (list of (s,a,r,s',done) tuples)
- Takes td_errors (list of TD-error magnitudes)
- Returns a batch of indices sampled with probability proportional to (priority + epsilon)^alpha

### Constraints

- alpha in [0,1]: interpolates between uniform (0) and max priority (1)
- Priorities are |TD-error| + epsilon
- Batch size is requested size
- Return indices, not transitions

### Hints

<details>
<summary>Hint 1: Normalize priorities</summary>
Priority_i = (|TD-error_i| + epsilon)^alpha. Normalize to sum to 1.
</details>

<details>
<summary>Hint 2: Sample with replacement</summary>
Use np.random.choice with probabilities.
</details>

<details>
<summary>Hint 3: Handle edge cases</summary>
Zero errors should have small nonzero priority.
</details>

## Theory

### The simple version

Transitions with high TD-error are surprising to your current estimate. Sample them more often to learn faster.

### The formula

P(i) ∝ (|TD-error_i| + ε)^α

where α controls how much to prioritize (0=uniform, 1=greedy).

### Importance sampling correction

When using PER, low-priority samples need upweighting during gradient updates to unbias the estimate. This requires tracking and applying importance weights.

### Why it helps

Learning focuses on hard examples. In practice, PER speeds up learning by 2-3x in many domains.

## Explanation

PER is a key component of DQN variants (Rainbow, Ape-X). It addresses a key RL challenge: learning from sparse, skewed experience distributions.
