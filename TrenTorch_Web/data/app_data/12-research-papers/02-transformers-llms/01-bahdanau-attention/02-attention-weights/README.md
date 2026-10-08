---
name: research-bahdanau-attention-weights
title: 'Bahdanau Attention: Turning Scores Into Weights'
tags: [research-papers, transformers, llm, attention]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Scores can be any real numbers, but attention needs weights that are positive and sum to one, so the model can average the encoder states. A softmax does that: it exponentiates each score and normalizes.

### From theory to code

Implement `attention_weights(scores)`, a numerically stable softmax over the score vector.

### Constraints

- Subtract the maximum before exponentiating to avoid overflow.

### Hints

<details>
<summary>Hint 1</summary>

Subtract `scores.max()` first, exponentiate, then divide by the sum.

</details>

## Theory

### The simple version

Subtracting the maximum doesn't change the result, since softmax is invariant to shifts, but it keeps the exponentials from overflowing for large scores.

### The formula

$$\alpha_j = \frac{\exp(e_j)}{\sum_k \exp(e_k)}$$

### How NumPy/PyTorch actually implements this

`torch.softmax(scores, dim=-1)` computes this in one call.

## Explanation

The max subtraction is the same trick used in every softmax implementation, including `torch.softmax`.
