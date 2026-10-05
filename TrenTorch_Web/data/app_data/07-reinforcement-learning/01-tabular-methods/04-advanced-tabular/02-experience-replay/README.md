---
title: Experience Replay Buffer
name: rl-experience-replay-buffer
difficulty: Intermediate
tags: [rl, experience-replay, memory, off-policy]
---

## Statement

Experience Replay stores transitions in a buffer and samples minibatches for training, breaking correlation in the data stream and enabling off-policy learning.

### The problem, from first principles

Online learning from a stream of correlated transitions (consecutive transitions from the same episode are similar) leads to instability and poor generalization. Replay breaks temporal correlation by shuffling experience.

### From theory to code

Implement `experience_replay_buffer(capacity)` class with:

- `add(s, a, r, s', done)` to store transitions
- `sample(batch_size)` to return random minibatch
- `__len__` for current size

### Constraints

- Buffer has fixed capacity (FIFO when full)
- Sample without replacement (or with if capacity < batch_size)
- Return dict or list of transitions

### Hints

<details>
<summary>Hint 1: Store transitions</summary>
Use a deque or list with max length.
</details>

<details>
<summary>Hint 2: Sample uniformly</summary>
Random choice without replacement from stored transitions.
</details>

<details>
<summary>Hint 3: Handle small buffers</summary>
If batch_size > buffer_size, sample with replacement.
</details>

## Theory

### The simple version

Keep a buffer of past experiences. When training, randomly sample minibatches from it instead of using fresh data.

### Why it helps

1. Breaks temporal correlation in data
2. Enables off-policy learning (train on old data)
3. Better sample efficiency (reuse data multiple times)
4. Stabilizes learning (less correlation in gradients)

### Buffer size tradeoff

Large: more stable, but stale data
Small: fresh data, but less stable

Typical: 10^4 to 10^6 transitions

## Explanation

Experience replay is the most important stabilization technique in deep RL. Without it, neural network agents diverge or learn slowly.
