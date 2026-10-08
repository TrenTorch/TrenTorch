---
name: research-ntm-content-weights
title: 'Neural Turing Machines: Content Addressing'
tags: [research-papers, sequence-models, memory, neural-computation]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Neural Turing Machines (Graves et al., 2014) read and write an external memory with differentiable attention. Content addressing finds memory rows similar to a key, using cosine similarity sharpened by a strength beta.

### From theory to code

Implement `content_weights(memory, key, beta)`, the softmax of beta times the cosine similarities.

### Constraints

- Cosine similarity is scale-invariant in the key.

### Hints

<details>
<summary>Hint 1</summary>

Compute each row's cosine similarity with the key, scale by beta, then take a stable softmax.

</details>

## Theory

### The simple version

The key picks out rows by content rather than by address, so the model can retrieve memories it finds similar to a query.

### The formula

$$w_i = \frac{\exp(\beta\,\cos(k, M_i))}{\sum_j \exp(\beta\,\cos(k, M_j))}$$

### How NumPy/PyTorch actually implements this

Memory-augmented networks implement this addressing as a softmax over normalized memory dot products.

## Explanation

Large beta gives a sharp, nearly one-hot focus; beta zero gives a uniform read over memory.
