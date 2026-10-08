---
name: research-zaremba-bptt-chunks
title: 'RNN Regularization: Truncated BPTT Chunks'
tags: [research-papers, sequence-models, language-modelling, regularization]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Training an RNN on a long text is split into truncated segments, and gradients only flow back through a fixed window. The number of segments per pass decides how often the hidden state is carried over.

### From theory to code

Implement `bptt_chunks(T, bptt)`, the number of truncated segments needed for a sequence.

### Constraints

- Round up for a partial last segment.

### Hints

<details>
<summary>Hint 1</summary>

Use ceiling division of the length by the truncation window.

</details>

## Theory

### The simple version

Truncation bounds the memory and compute of backpropagation, and the carried hidden state keeps long-range context across chunks.

### The formula

$$K = \left\lceil\frac{T}{b}\right\rceil$$

### How NumPy/PyTorch actually implements this

Language-model training loops split the token stream into fixed-length windows with this count.

## Explanation

The hidden state is detached between chunks, so gradients never cross chunk boundaries.
