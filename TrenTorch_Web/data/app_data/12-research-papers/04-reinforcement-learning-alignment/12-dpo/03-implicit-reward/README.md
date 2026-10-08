---
name: research-dpo-implicit-reward
title: 'DPO: The Implicit Reward'
tags: [research-papers, reinforcement-learning, alignment, dpo]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

DPO's key identity is that the reward a policy implicitly assigns to a response is beta times its log-ratio against the reference. Looking at this implicit reward explains why DPO needs no separate reward model.

### From theory to code

Implement `implicit_reward(logp, ref, beta)`, returning `beta * (logp - ref)`.

### Constraints

- Works element-wise on arrays.

### Hints

<details>
<summary>Hint 1</summary>

Subtract the reference log-probabilities and multiply by `beta`.

</details>

## Theory

### The simple version

A response that the policy has made more likely than the reference earns a positive implicit reward. That is the quantity the DPO loss compares across winners and losers.

### The formula

$$\hat r(x, y) = \beta\log\frac{\pi_\theta(y\mid x)}{\pi_{\text{ref}}(y\mid x)}$$

### How NumPy/PyTorch actually implements this

The DPO logging code reports this implicit reward for chosen and rejected responses to track training.

## Explanation

This is the reward that makes the optimal KL-constrained policy equal to the reference times exp of reward over beta.
