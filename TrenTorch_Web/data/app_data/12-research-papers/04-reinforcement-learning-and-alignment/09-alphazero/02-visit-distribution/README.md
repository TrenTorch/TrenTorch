---
name: research-alphazero-visit-distribution
title: 'AlphaZero: The Visit Distribution'
tags: [research-papers, reinforcement-learning, self-play, search]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

After search, AlphaZero uses the visit counts of the root moves as the training target for the policy. A temperature controls how sharp that target is: high temperature explores, low temperature plays the most-visited move.

### From theory to code

Implement `visit_distribution(counts, tau)`, returning the normalized counts raised to `1 / tau`.

### Constraints

- Counts are positive.

### Hints

<details>
<summary>Hint 1</summary>

Raise each count to `1 / tau`, then divide by the total.

</details>

## Theory

### The simple version

The visit counts summarize what the search learned about each move. Raising them to a power sharpens or flattens the distribution without changing their order.

### The formula

$$\pi(a) = \frac{N(s,a)^{1/\tau}}{\sum_b N(s,b)^{1/\tau}}$$

### How NumPy/PyTorch actually implements this

Self-play loops record this distribution as the policy label for every position in the game.

## Explanation

At tau = 1 the target is proportional to the visits. As tau goes to zero it becomes one-hot on the most visited move.
