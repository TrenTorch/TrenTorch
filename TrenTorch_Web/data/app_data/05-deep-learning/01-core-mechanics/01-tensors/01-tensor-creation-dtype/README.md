---
name: dl-tensor-tensor-creation-dtype
title: 'Tensor Creation and Data Types'
tags: [deep-learning, tensor-ops]
difficulty: Beginner
---

## Statement

Create tensors with different data types (float32, int64, bool) and shapes. Understand how dtype affects memory, precision, and computation. Initialize tensors via zeros, ones, random values, or from Python lists.

## Theory

### Tensors are multi-dimensional arrays

A tensor is the fundamental data structure in deep learning: a generalization of vectors and matrices to any number of dimensions.

- 0D: scalar (single number)
- 1D: vector (list of numbers)
- 2D: matrix (rows and columns)
- 3D+: higher-dimensional arrays (batches, sequences, spatial dimensions)

### Data types (dtypes)

- loat32: default for neural networks (32-bit floating point, ~7 decimal digits precision)
- loat64: higher precision, twice the memory
- int32, int64: integers, for indices and counts
- ool: True/False values
- complex64, complex128: complex numbers

### Tensor creation patterns

`python
torch.zeros(3, 4)          # All zeros
torch.ones(2, 5)           # All ones
torch.randn(3, 3)          # Random normal distribution
torch.arange(10)           # 0, 1, 2, ..., 9
torch.tensor([1, 2, 3])    # From Python list
torch.full((2, 3), 7)      # All elements = 7
`

### Why dtype matters

- **Memory**: float32 = 4 bytes/element; float64 = 8 bytes
- **Precision**: float32 sufficient for most deep learning
- **GPU efficiency**: GPUs optimized for float32
- **Mixed precision training**: float32 compute + float16 memory

## Explanation

Solutions demonstrate creating tensors with different shapes and dtypes, checking memory footprint, and understanding how dtype affects computation precision. Key insight: choose dtype based on trade-offs between precision, memory, and speed.
