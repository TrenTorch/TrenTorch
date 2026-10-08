---
name: research-las-sequence-nll
title: 'Listen, Attend and Spell: Character Negative Log-Likelihood'
tags: [research-papers, sequence-models, speech, attention]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

LAS decodes characters with an attention decoder trained by maximum likelihood. The training loss is the sum of the negative log-probabilities of the correct characters, the same sequence loss as in machine translation.

### From theory to code

Implement `char_nll(logp, targets)`, the summed negative log-likelihood of the transcript.

### Constraints

- Returns a Python float.

### Hints

<details>
<summary>Hint 1</summary>

Pick the log-probability of the correct character at each step, negate, and sum.

</details>

## Theory

### The simple version

Character-level outputs make the model open-vocabulary, and the summed loss trains it to spell the transcript.

### The formula

$$\mathcal{L} = -\sum_{s=1}^{S}\log p(y_s \mid y_{<s}, X)$$

### How NumPy/PyTorch actually implements this

Speech decoders in toolkits compute the same character cross-entropy on their output layer.

## Explanation

The sum runs over output characters, while the attention reads the pyramidal encoder states.
