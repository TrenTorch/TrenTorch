---
name: dl-generative-maskgit
title: MaskGIT
tags: [deep-learning, generative-models, maskgit]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

MaskGIT is an iterative generative model using masked token prediction. During training, tokens are randomly masked and a transformer predicts them. During generation, tokens with highest uncertainty are iteratively refined in parallel.

Training loss is standard cross-entropy on masked positions. The key is the masking schedule and iterative refinement strategy.

$$\mathcal{L} = \sum_i \mathbb{1}[\text{token}_i \text{ masked}] \cdot H(\text{pred}_i, \text{target}_i)$$

### From theory to code

Implement:

```python
maskgit_loss(logits, targets, mask)
```

Computes cross-entropy loss only on masked token positions.

### Constraints

- logits shape: (N, L, V) where V is vocab size.
- targets shape: (N, L).
- mask shape: (N, L), binary.
- Return scalar loss.

## Theory

MaskGIT enables fast iterative generation by predicting multiple tokens in parallel at each step, unlike autoregressive models. Useful for image and text generation.

## Explanation

Compute cross-entropy loss per token. Zero out loss for unmasked positions. Average over batch and masked positions.
