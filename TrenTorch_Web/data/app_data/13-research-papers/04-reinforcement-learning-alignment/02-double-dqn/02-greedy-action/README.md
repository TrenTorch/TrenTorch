---
name: research-double-dqn-greedy-action
title: 'Double DQN: The Greedy Action'
tags: [research-papers, reinforcement-learning, deep-q-learning]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The greedy action is the one with the highest estimated value. Both networks in Double DQN use this rule, so getting its tie-breaking right matters for reproducible targets.

### From theory to code

Implement `greedy_action(q)`, returning the index of the largest action value.

### Constraints

- Return a Python `int`.

### Hints

<details>
<summary>Hint 1</summary>

Use `np.argmax`, which breaks ties by the lowest index.

</details>

## Theory

### The simple version

The greedy choice is the core of control with value functions. Ties going to the lowest index keeps behaviour deterministic.

### The formula

$$a^* = \arg\max_a Q(s, a)$$

### How NumPy/PyTorch actually implements this

`torch.argmax` implements the same selection on batched Q-values.

## Explanation

This is the policy that epsilon-greedy exploration follows most of the time.
