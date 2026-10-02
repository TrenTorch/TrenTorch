---
name: numpy-assemble-linear-layer-and-attention
title: 'Assemble: A Mini Linear Layer and Attention Weights with Tensor-Style Metadata'
tags: [numpy-tensors]
difficulty: Advanced
---

## Statement

Implement the building blocks of a tiny neural-network layer and the attention-weight computation using ndarrays with tensor-style metadata, combining random initialization, matrix multiplication, broadcasting, aggregation along an axis, dtype and device rules, and gradient-flag propagation.

## Theory

This problem introduces no new concepts. It combines:

- **He initialization** from a seeded `Generator`.
- Casting weights to the tensor default `float32`, and enforcing the same-device rule.
- Parameters tracked (`requires_grad=True`), with the output's flag following the propagation rule.
- A linear layer: $Y = XW + b$, where the matrix product has shape `(batch, out)` and the bias of shape `(out,)` broadcasts across the batch.
- Attention weights: a row-wise softmax of $QK^\top / \sqrt{d}$, computed with `axis=1` aggregation and `np.newaxis`, using the max-subtraction trick for numerical stability:

$$
\frac{e^{S_{ij} - m_i}}{\sum_k e^{S_{ik} - m_i}} = \frac{e^{S_{ij}}}{\sum_k e^{S_{ik}}}
$$

## Explanation

`init_linear_params` draws `W` with `rng.normal(0.0, sqrt(2/in_features), (in, out))`, casts to `float32`, and builds `b` as `np.zeros(out_features, dtype=np.float32)` — both wrapped as records with `requires_grad=True` and the given device. `linear_forward` checks all three devices match and that `x`'s trailing dimension equals `W`'s leading dimension, then computes `x_data @ W_data + b_data` (bias broadcasts over rows automatically), with `requires_grad` propagated via OR across all three inputs. `attention_weights` computes `scores = (q @ k.T) / sqrt(d)`, subtracts each row's max (`scores - scores.max(axis=1, keepdims=True)`) before exponentiating, then divides by each row's sum (`exp_scores / exp_scores.sum(axis=1, keepdims=True)`) — entirely vectorized, no loops.
