---
name: dl-tensor-reduction-ops
title: 'Reduction Operations (Sum, Mean, Max)'
tags: [deep-learning, tensor-ops]
difficulty: Beginner
---

## Statement

Reduce tensors along axes: sum all, sum per row/column, mean, max, min. Understand keepdims parameter. Handle empty dimensions.

## Theory

### Reductions collapse dimensions

Sum, mean, max, min combine elements along an axis:

`python
a = torch.randn(3, 4, 5)
b = a.sum()                    # Single number (sum all)
c = a.sum(dim=0)               # Shape (4, 5) - sum across batch
d = a.sum(dim=1)               # Shape (3, 5) - sum across 4 elements
e = a.sum(dim=[0, 2])          # Shape (4,) - sum across batch and last
`

### keepdims preserves dimensions

`python
a = torch.randn(3, 4, 5)
b = a.sum(dim=1, keepdim=True) # Shape (3, 1, 5) - broadcasts easily
c = b / a.sum(dim=1, keepdim=True)  # Softmax-like normalization
`

### Common reductions

- sum(): total
- mean(): average
- max(), min(): extremes
- std(): standard deviation
- ar(): variance
-

orm(): L1, L2, etc.

### Why reductions matter

- Aggregation: batch mean loss for training
- Normalization: sum to 1 for probabilities, mean=0 std=1 for inputs
- Monitoring: track gradient norms, loss across batches
- Pooling: max pooling in CNNs

## Explanation

Solutions aggregate tensors along axes, use keepdims for broadcasting-friendly shapes, and compute statistics per batch/channel. Key insight: dim parameter crucial - wrong axis gives wrong result.
