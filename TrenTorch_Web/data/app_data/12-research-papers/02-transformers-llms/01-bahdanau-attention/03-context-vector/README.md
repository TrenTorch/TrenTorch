---
name: research-bahdanau-context-vector
title: 'Bahdanau Attention: The Context Vector'
tags: [research-papers, transformers, llm, attention]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Once the weights are known, the context vector is the weighted average of the encoder states. It gives the decoder one summary of the input that is tailored to the word it is about to produce.

### From theory to code

Implement `context_vector(weights, H)`, which returns the weighted sum of the encoder states.

### Constraints

- Weights sum to 1 across the `T` positions.

### Hints

<details>
<summary>Hint 1</summary>

Use a matrix product: weights of shape `(T,)` times states of shape `(T, d)`.

</details>

## Theory

### The simple version

A context vector that puts all weight on one state copies that state. Spreading the weight blends several states, which lets the decoder use information from many input positions at once.

### The formula

$$c_i = \sum_{j} \alpha_{ij}\,h_j$$

### How NumPy/PyTorch actually implements this

`weights @ H` in NumPy or `torch.bmm` for batches computes the same weighted sum.

## Explanation

This is the attention step itself: a convex combination of encoder states, with the coefficients from the softmax.
