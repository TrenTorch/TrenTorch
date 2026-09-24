---
name: numpy-assemble-extract-and-modify
title: 'Assemble: Extract and Modify a Data Selection'
tags: [numpy-core]
difficulty: Advanced
---

## Statement

Implement a single function that combines every selection method from this module — basic indexing, slicing, boolean masking, fancy indexing, and `np.where` — into one realistic data-cleaning task, while correctly tracking which operations return views and which return copies.

## Theory

This problem introduces no new concepts. It combines every topic covered in this module into one function, matching the "assemble" pattern used elsewhere on TrenTorch.

Specifically, this requires:

- Using slicing to extract a sub-region of an array.
- Using `np.where` to replace invalid values in that region.
- Using fancy indexing to reorder a specific set of columns.
- Correctly reasoning about which steps mutate a shared buffer (views) versus which produce an independent copy — this is graded directly, not just the final values.

Re-read the earlier topics in this module if a specific requirement below is unclear.

## Explanation

`region = data[row_range[0]:row_range[1], :]` is a slice, so it's a view — it shares memory with `data`. `cleaned = np.where(region < 0, 0, region)` always builds a new array, so it's independent of `region`. `reordered = cleaned[:, priority_indices]` is fancy indexing on the column axis, also independent. The two `_shares_memory` flags are reported using `np.shares_memory(a, b)`, which checks the underlying buffer directly rather than relying on assumptions about which operation was used.
