---
name: research-sat-hard-sample
title: 'Show, Attend and Tell: Sampling Hard Attention'
tags: [research-papers, sequence-models, attention, captioning]
difficulty: Advanced
---

## Statement

### The problem, from first principles

The hard variant of attention in Show, Attend and Tell samples one location per word rather than averaging. It is not differentiable, so the paper trains it with a score-function gradient estimator.

### From theory to code

Implement `sample_hard_attention(alpha, rng)`, drawing one location from the attention distribution.

### Constraints

- Use the supplied `rng` for reproducibility.

### Hints

<details>
<summary>Hint 1</summary>

Call the generator's choice with the attention distribution as probabilities.

</details>

## Theory

### The simple version

Sampling makes the model commit to a region, which can be sharper than soft averaging but needs a higher-variance gradient.

### The formula

$$z_t \sim \text{Categorical}(\alpha_{t,1}, \ldots, \alpha_{t,L})$$

### How NumPy/PyTorch actually implements this

Hard attention training code draws one location per step from the same categorical distribution.

## Explanation

The sampled index selects one feature vector; the soft context is the expectation over this choice.
