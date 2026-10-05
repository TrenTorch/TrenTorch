---
name: problem-43-rolling-mean
title: 'Rolling Mean'
tags: [problemset, data-stats-for-ds, time-series]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'time series'
hint: 'maintain a running sum and remove the value leaving the window'
tools: [NumPy]
---

## Statement

Implement `solve(x, window)`. Compute a trailing mean over a fixed-width window. Positions with fewer than window observations are NaN.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0, 4.0], 2)
```

Output:

```text
[nan, 1.5, 2.5, 3.5]
```

**Example 2**

Input:

```python
solve([2.0, 4.0, 6.0], 3)
```

Output:

```text
[nan, nan, 4.0]
```

## Theory

For each complete trailing window, average its window values; a running sum computes these means efficiently.

## Explanation

The output is computed from the supplied observations using the method above. Values and arrays are passed directly as arguments; the function returns its result without printing.
