---
name: problem-42-time-series-lag-feature
title: 'Time-Series Lag Feature'
tags: [problemset, data-stats-for-ds, time-series]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'time series'
hint: 'shift values right and mark the first row missing'
tools: [NumPy]
---

## Statement

Implement `solve(x)`. Return a one-step lag feature for an ordered numeric series; the first position is NaN because it has no preceding value.

### Examples

**Example 1**

Input:

```python
solve([10.0, 20.0, 30.0, 40.0])
```

Output:

```text
[nan, 10.0, 20.0, 30.0]
```

**Example 2**

Input:

```python
solve([3.0, 8.0])
```

Output:

```text
[nan, 3.0]
```

## Theory

A lag shifts each observation one position later while leaving the first entry undefined.

## Explanation

The output is computed from the supplied observations using the method above. Values and arrays are passed directly as arguments; the function returns its result without printing.
