---
name: research-a3c-entropy
title: 'A3C: Policy Entropy'
tags: [research-papers, reinforcement-learning, actor-critic, asynchronous]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The entropy of the action distribution measures how random the policy is. Adding an entropy bonus to the objective keeps the policy exploring instead of collapsing onto one action too early.

### From theory to code

Implement `entropy(p)`, the Shannon entropy of a discrete distribution, with the convention that zero probabilities contribute zero.

### Constraints

- Use the natural logarithm.

### Hints

<details>
<summary>Hint 1</summary>

Compute `-p log p` element-wise, treating zero entries as zero, then sum.

</details>

## Theory

### The simple version

A uniform policy has the maximum entropy for its number of actions, and a deterministic one has none. The bonus pulls the policy toward the uniform end.

### The formula

$$H(\pi) = -\sum_a \pi(a)\log\pi(a), \qquad 0\log 0 := 0$$

### How NumPy/PyTorch actually implements this

`torch.distributions.Categorical(probs).entropy()` computes the same quantity.

## Explanation

The convention 0 log 0 = 0 is the limit of x log x as x goes to zero, which the code applies by masking.
