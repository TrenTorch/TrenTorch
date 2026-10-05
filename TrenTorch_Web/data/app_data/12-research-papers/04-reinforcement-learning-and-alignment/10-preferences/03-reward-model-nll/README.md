---
name: research-preference-reward-nll
title: 'Human Preferences: The Reward Model Loss'
tags: [research-papers, reinforcement-learning, alignment, reward-learning]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Training the reward model is a binary classification problem: given two segments and a human label, maximize the probability of the label. The loss is the negative log-likelihood of that label under the preference model.

### From theory to code

Implement `reward_model_nll(y, r_a, r_b)`, the negative log-likelihood of the human label.

### Constraints

- Clamp probabilities away from 0 and 1 for numerical safety.

### Hints

<details>
<summary>Hint 1</summary>

Compute `p = sigmoid(r_a - r_b)`, then the binary cross-entropy against `y`.

</details>

## Theory

### The simple version

A correct confident prediction costs almost nothing, while a confident mistake is penalized heavily. Minimizing this loss makes the reward model agree with the human labels.

### The formula

$$\mathcal{L} = -\big[y\log p + (1-y)\log(1-p)\big], \qquad p = \sigma(r_A - r_B)$$

### How NumPy/PyTorch actually implements this

Reward model training uses `binary_cross_entropy_with_logits` on the reward difference, which matches this loss.

## Explanation

This is binary cross-entropy on the logit `r_a - r_b`, the same form used for any pairwise preference classifier.
