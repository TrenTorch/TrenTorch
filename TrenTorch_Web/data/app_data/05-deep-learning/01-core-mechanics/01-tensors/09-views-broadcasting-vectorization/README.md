---
name: dl-tensor-views-broadcasting-vectorization
title: 'Views, Broadcasting, and Vectorization'
tags: [deep-learning, tensor-ops]
difficulty: Beginner
---

## Statement

Master the combination of views (shared memory), broadcasting (shape expansion), and vectorization. Avoid Python loops; express operations on entire tensors.

## Theory

### Views: efficient memory sharing

`python
a = torch.arange(6)
b = a.view(2, 3)       # View: (2, 3) shape, same memory
b[0, 0] = 99           # Changes a[0]
c = a.view(-1, 1)      # Infer dimension: (6, 1)
`

### Broadcasting: automatic expansion

`python
a = torch.randn(3, 1, 4)
b = torch.randn(1, 5, 4)
c = a + b              # Broadcasts to (3, 5, 4)
`

### Vectorization vs loops

`python
# Slow (Python loop)
result = []
for i in range(1000):
    result.append(a[i] * b[i])

# Fast (vectorized)
result = a * b         # Single operation on entire tensors
`

### Combining views, broadcasting, vectorization

`python
images = torch.randn(32, 3, 224, 224)        # (B, C, H, W)
mean = torch.randn(3, 1, 1)                  # (C, 1, 1)
normalized = (images - mean) / std           # Broadcasting: (32, 3, 224, 224)
`

### Why vectorization matters

- Speed: GPU parallelism only works on entire operations
- Code clarity: no explicit loops obscuring intent
- Memory efficiency: one large operation often faster than many small ones
- Debugging: easier to trace tensor operations than loop logic

## Explanation

Solutions combine views for memory efficiency, broadcasting for shape flexibility, and vectorization to avoid loops. Key insight: if you write a for loop over batch, vectorize it instead.
