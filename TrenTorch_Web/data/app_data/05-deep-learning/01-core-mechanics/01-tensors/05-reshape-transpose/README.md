---
name: dl-tensor-reshape-transpose
title: 'Reshape and Transpose'
tags: [deep-learning, tensor-ops]
difficulty: Beginner
---

## Statement

Reshape tensors to new shapes while preserving element count. Transpose axes to swap dimensions. Understand how reshaping affects strides and memory layout.

## Theory

### Reshape changes dimensions without changing data

Reshape reinterprets a tensor's elements into a new shape (total elements unchanged):

`python
a = torch.arange(12)          # shape (12,)
b = a.reshape(3, 4)           # shape (3, 4)
c = a.reshape(2, 3, 2)        # shape (2, 3, 2)
d = a.reshape(-1, 4)          # -1 infers dimension: (3, 4)
`

### Transpose swaps axes

`python
a = torch.randn(3, 4, 5)
b = a.transpose(0, 2)         # Swap axes 0 and 2 → (5, 4, 3)
c = a.T                        # For 2D: transpose last two dims
d = a.permute(2, 0, 1)        # Arbitrary reordering → (5, 3, 4)
`

### Reshape vs view vs permute

-

eshape(): may copy memory; more flexible

- iew(): cheap (no copy); requires C-contiguous; fails if strides incompatible
- permute(): reorders axes; creates new strides

### Why reshape/transpose matter

- Batching: add batch dimension for vectorized computation
- Flattening: convert image (H, W, C) to vector for fully connected layer
- Swapping: move sequence to different axis for different operations
- Merging/splitting: group dimensions for distributed training

## Explanation

Solutions reshape tensors for different computations (flatten for FC layers, reshape for batching) and transpose for axis-specific operations. Key insight: understand element layout (row-major) to predict reshape outcomes.
