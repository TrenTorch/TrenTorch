---
name: dl-tensor-matmul
title: 'Matrix Multiplication (Matmul)'
tags: [deep-learning, tensor-ops]
difficulty: Beginner
---

## Statement

Implement and understand matrix multiplication. Compute (m×n) × (n×p) = (m×p). Handle batched matmul: (B×m×n) × (B×n×p) = (B×m×p). Understand why matmul differs from element-wise *.

## Theory

### Matrix multiplication is not element-wise

Matmul combines rows and columns via dot products:

`A (3×2) @ B (2×4) = C (3×4)
C[i, j] = sum(A[i, k] * B[k, j] for all k)`

### Matmul vs element-wise *

`python
A * B  # Element-wise multiplication
A @ B  # Matrix multiplication (dot products)
`

### Broadcasting in matmul

Matmul broadcasts batch dimensions:

`python
A: (B, m, n)
B: (B, n, p)
Result: (B, m, p)  # Compute B independent matmuls
`

### Time complexity

Matmul is expensive: O(m × n × p) for (m×n) × (n×p).

For (3000, 3000) × (3000, 3000): ~27 billion multiplications.

Optimization (GPU kernels, quantization) is critical for large models.

### Why matmul matters

- Core operation in neural networks (linear layers, attention, convolutions)
- Efficiency heavily impacts training speed (GPUs optimized for matmul)
- Understanding shapes crucial for debugging

## Explanation

Solutions compute matmul correctly, track dimension changes through the network, and recognize matmul as the bottleneck in deep learning. Key insight: shape of result is (batch, m, p) from (batch, m, n) @ (batch, n, p).
