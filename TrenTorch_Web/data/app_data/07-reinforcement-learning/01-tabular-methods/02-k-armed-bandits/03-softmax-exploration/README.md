---
name: k-armed-bandits-softmax-exploration
title: Softmax (Boltzmann) exploration
tags: [reinforcement-learning, bandits, exploration]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Epsilon-greedy explores uniformly: it is as likely to try a terrible arm as a nearly-best one. Softmax exploration instead picks arms with probability that grows with their estimated value, so promising arms are tried more and clearly bad ones rarely.

### From theory to code

Implement `softmax_probabilities(q_values, temperature)` returning the probability of choosing each arm.

### Constraints

- `q_values` is a one-dimensional float array; `temperature` is a positive float.
- Return a float array of the same length that sums to 1.
- Must not overflow for large `q_values / temperature`: subtract the maximum before exponentiating.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Divide the values by the temperature, subtract the maximum, exponentiate, then normalise.

</details>

<details><summary>Hint 2</summary>

Subtracting a constant from every logit does not change the softmax, but it keeps `exp` from overflowing.

</details>

## Theory

### The simple version

The temperature is a dial. High temperature flattens the probabilities towards uniform (lots of exploring); low temperature sharpens them towards always picking the best arm.

### The formula

$$P(a) = \frac{\exp\big(Q(a)/\tau\big)}{\sum_{b} \exp\big(Q(b)/\tau\big)}$$

### How libraries implement this

`scipy.special.softmax` and `torch.softmax` apply the same max-subtraction trick internally.

## Explanation

Subtracting the maximum makes the largest exponent exactly zero, so no term can overflow, and the normalisation cancels the shift, leaving the probabilities unchanged.
