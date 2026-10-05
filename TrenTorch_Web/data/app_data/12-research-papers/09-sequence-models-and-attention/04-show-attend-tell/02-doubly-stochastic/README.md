---
name: research-sat-doubly-stochastic
title: 'Show, Attend and Tell: Doubly Stochastic Penalty'
tags: [research-papers, sequence-models, attention, captioning]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Show, Attend and Tell adds a regularizer that encourages the attention to cover the whole image over the caption. Summed over the words, each location's attention should be about one, which is a doubly stochastic constraint.

### From theory to code

Implement `doubly_stochastic_penalty(alpha)`, the squared deviation of each location's total attention from one.

### Constraints

- Columns of alpha are locations.

### Hints

<details>
<summary>Hint 1</summary>

Sum the attention matrix over the words for each location, subtract from one, square, and sum.

</details>

## Theory

### The simple version

Without the penalty the model can attend to a few regions for every word, missing objects in the scene. The penalty spreads attention so each object gets described.

### The formula

$$\mathcal{L}_{\text{reg}} = \lambda\sum_{i=1}^{L}\Big(1 - \sum_{t=1}^{T}\alpha_{t,i}\Big)^2$$

### How NumPy/PyTorch actually implements this

Captioning training code adds this term to the cross-entropy over the caption.

## Explanation

The regularizer is added to the captioning loss with a small weight.
