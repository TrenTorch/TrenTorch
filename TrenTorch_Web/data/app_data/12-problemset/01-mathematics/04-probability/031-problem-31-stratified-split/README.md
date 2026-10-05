---
name: problem-31-stratified-split
title: 'Stratified Split'
tags: [problemset, data-stats-for-ds, sampling]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability'
topic: 'sampling'
hint: 'shuffle indices within each class then allocate each class separately'
tools: [NumPy]
---

## Statement

Implement `solve(y, test_size=0.2, seed=0)`. Split sample indices into deterministic train and test arrays while shuffling within each class. The test count in each class is floor(class_size*test_size).

### Examples

**Example 1**

Input:

```python
solve([0,0,0,0,1,1,1,1], 0.5, seed=0)
```

Output:

```text
([1, 3, 4, 5], [0, 2, 6, 7])
```

**Example 2**

Input:

```python
solve([0,0,0,0,0,1,1,1,1,1], 0.4, seed=2)
```

Output:

```text
([0, 1, 3, 6, 8, 9], [2, 4, 5, 7])
```

## Theory

Stratification samples each class separately, preserving its proportion as closely as the per-class integer test count permits.

## Explanation

The output is computed from the supplied observations using the method above. Values and arrays are passed directly as arguments; the function returns its result without printing.
