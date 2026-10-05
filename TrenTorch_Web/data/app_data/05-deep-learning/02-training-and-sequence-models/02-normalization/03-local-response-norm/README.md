---
name: dl-training-local-response-norm
title: Local Response Normalization
tags: [deep-learning, training, normalization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Local Response Normalization (LRN) normalizes each activation using responses of neighboring channels. Useful in early CNNs for competitive inhibition. For each position, normalization is based on a local neighborhood across channels.

$$\text{lrn}(x, k, \alpha, \beta, n) = x \left(k + \alpha \sum_{i=\max(0, c-n/2)}^{\min(C-1, c+n/2)} x_i^2\right)^{-\beta}$$

Where the sum is over n neighboring channels (spatial location fixed).

### From theory to code

Implement:

```python
local_response_norm(x, k=2.0, alpha=1e-4, beta=0.75, n=5)
```

### Constraints

- x shape: (N, C, H, W)
- k, alpha, beta, n are positive floats
- n is the size of neighborhood (odd).
- Return normalized x, same shape.

## Theory

LRN encourages sparse activation and lateral inhibition. Modern batch norm largely replaced it, but it remains useful in some architectures.

## Explanation

For each channel, sum squared activations in a local neighborhood (within n/2 channels). Apply normalization factor to the activation.
