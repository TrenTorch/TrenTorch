---
name: dl-tensor-assemble-linear-layer-and-attention
title: 'Assemble Linear Layers and Attention'
tags: [deep-learning, tensor-ops]
difficulty: Beginner
---

## Statement

Use tensor operations to implement a linear layer (y = xW^T + b) and scaled dot-product attention. Understand how tensor ops combine into meaningful neural network components.

## Theory

### Linear layer: y = xW^T + b

`python
x = torch.randn(32, 10)      # Batch of 32, feature dim 10
W = torch.randn(5, 10)       # Output dim 5, input dim 10
b = torch.randn(5)           # Bias

y = x @ W.T + b              # (32, 10) @ (10, 5) + (5,) = (32, 5)
`

Matmul computes dot products per output neuron; addition broadcasts bias.

### Scaled dot-product attention

`python
Q = torch.randn(batch, seq_len, d_k)
K = torch.randn(batch, seq_len, d_k)
V = torch.randn(batch, seq_len, d_v)

scores = Q @ K.T / math.sqrt(d_k)         # (B, seq, seq)
attn_weights = torch.softmax(scores, dim=-1)
output = attn_weights @ V                  # (B, seq, d_v)
`

Matmul computes attention scores; softmax normalizes; output is weighted sum of values.

### Why understanding ops matters

- Debugging: know what each shape should be
- Optimization: choose efficient operations
- Novel architectures: combine ops creatively
- Understanding: not just use black-box layers, understand what happens

### Building blocks for neural networks

Linear layers, attention, pooling, normalization all combine:
- Matmul (core computation)
- Softmax/ReLU (nonlinearities)
- Reductions (aggregation)
- Reshaping (flexibility)

## Explanation

Solutions assemble linear layers and attention from tensor ops, verifying shapes at each step. Key insight: neural networks are compositions of vectorized tensor operations; mastering ops unlocks understanding.
