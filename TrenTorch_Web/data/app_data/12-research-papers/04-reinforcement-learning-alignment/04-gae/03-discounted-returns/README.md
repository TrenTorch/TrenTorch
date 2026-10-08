---
name: research-gae-discounted-returns
title: 'GAE: Discounted Returns'
tags: [research-papers, reinforcement-learning, policy-gradient, advantage]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The return from a step is the total discounted reward collected from there on. It is the quantity policy-gradient methods weight their updates by, in the simplest (REINFORCE) form.

### From theory to code

Implement `discounted_returns(rewards, gamma)`, computing the discounted return from each step.

### Constraints

- Compute from the last step backward.

### Hints

<details>
<summary>Hint 1</summary>

Start at zero after the final step and add `r_t + gamma` times the return from the next step.

</details>

## Theory

### The simple version

Recent rewards matter more than distant ones, and the discount factor controls how far ahead the agent looks. The backward pass gives every step its full future in linear time.

### The formula

$$G_t = \sum_{k=0}^{T-t-1} \gamma^k\, r_{t+k}$$

### How NumPy/PyTorch actually implements this

`scipy.signal.lfilter` computes the same discounted cumulative sum in vectorized form.

## Explanation

The recursion `G_t = r_t + gamma G_{t+1}` is the same identity the Bellman equation uses for values.
