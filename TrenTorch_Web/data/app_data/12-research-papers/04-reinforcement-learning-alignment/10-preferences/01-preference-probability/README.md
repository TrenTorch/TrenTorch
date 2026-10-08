---
name: research-preference-probability
title: 'Human Preferences: The Preference Probability'
tags: [research-papers, reinforcement-learning, alignment, reward-learning]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Christiano et al. (2017) learned a reward function from human comparisons instead of hand-written rewards. Humans watch two short clips and say which is better. The model turns reward differences into a probability of preference, and that probability is fitted to the human choices.

### From theory to code

Implement `preference_probability(r_a, r_b)`, returning `sigmoid(r_a - r_b)`.

### Constraints

- Preference depends only on the reward difference.

### Hints

<details>
<summary>Hint 1</summary>

Compute the logistic function of the difference.

</details>

## Theory

### The simple version

This is the Bradley-Terry model: each option has a latent score, and the chance of picking one over another is the logistic of the score gap.

### The formula

$$P(A \succ B) = \frac{\exp(r_A)}{\exp(r_A) + \exp(r_B)} = \sigma(r_A - r_B)$$

### How NumPy/PyTorch actually implements this

Reward-modelling code evaluates this sigmoid on the difference of predicted returns for each labelled pair.

## Explanation

The equality of the two forms is why the difference is the only thing that matters.
