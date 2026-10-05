---
name: problem-33-two-sample-difference-in-means
title: 'Two-Sample Difference in Means'
tags: [problemset, data-stats-for-ds, hypothesis-testing]
difficulty: Advanced
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'hypothesis testing'
hint: 'mean(A)-mean(B)'
tools: [NumPy]
---

## Statement

Implement `solve(a, b)`. Compute the difference between the mean of sample a and the mean of sample b.

### Examples

**Example 1**

Input:

```python
solve([2.0, 4.0, 6.0], [1.0, 2.0, 3.0])
```

Output:

```text
2.0
```

**Example 2**

Input:

```python
solve([1.0, 1.0], [3.0, 5.0])
```

Output:

```text
-3.0
```

## Theory

The estimated difference is the arithmetic mean of a minus the arithmetic mean of b.

## Explanation

The output is computed from the supplied observations using the method above. Values and arrays are passed directly as arguments; the function returns its result without printing.
