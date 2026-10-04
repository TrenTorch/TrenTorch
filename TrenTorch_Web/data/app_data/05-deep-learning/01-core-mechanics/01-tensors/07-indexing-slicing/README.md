---
name: dl-tensor-indexing-slicing
title: 'Indexing and Slicing'
tags: [deep-learning, tensor-ops]
difficulty: Beginner
---

## Statement

Extract sub-tensors via integer indexing, slicing, and boolean masks. Use advanced indexing for gather/scatter operations. Understand copy vs view behavior.

## Theory

### Indexing selects individual elements; slicing extracts sub-tensors

`python
a = torch.arange(24).reshape(2, 3, 4)
a[0]           # First element (first 3×4 matrix)
a[0, 1]        # Element at (0, 1)
a[0, 1, 2]     # Single element
a[:, 1]        # All rows, index 1 in second dim → (2, 4)
a[0:1, :, 2]   # Rows 0-0, all cols, index 2 in third → (1, 3)
`

### Slicing with step

`python
a = torch.arange(10)
a[::2]         # Every 2nd element → [0, 2, 4, 6, 8]
a[1::3]        # Start at 1, every 3rd → [1, 4, 7]
a[::-1]        # Reverse
`

### Boolean indexing

`python
mask = a > 5
a[mask]        # Elements where mask is True (1D result)
`

### Advanced indexing

`python
indices = torch.tensor([0, 2, 1])
a[indices]     # Gather: select in this order
a[indices] = 99  # Scatter: set selected elements
`

### Copy vs view

`python
b = a[0:5]     # View: shares memory; modifying b changes a
c = a[0:5].clone()  # Copy: independent data
`

### Why indexing matters

- Data extraction: select samples from batch
- Masking: filter by condition (loss items, valid predictions)
- Gathering: efficient reordering (needed for ranking, top-K)
- Advanced indexing: complex selection patterns

## Explanation

Solutions demonstrate integer/slice indexing, boolean masking for conditional selection, and advanced indexing for gather/scatter. Key insight: understand memory sharing (view) vs independence (clone).
