---
name: problem-42-time-series-lag-feature
title: 'Time-Series Lag Feature'
tags: [problemset, data-stats-for-ds, time-series]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'time series'
hint: 'shift right by one and put NaN in the first slot'
tools: [NumPy]
---

## Statement

Build a one-step lag feature from an ordered, non-empty numeric series: position $t$ holds the value from position $t-1$, and position $0$ has no predecessor so it is `NaN`.

Implement `solve(x)`.

**Returns.** Return a float NumPy array of the same length as the input.

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
solve([7.0])
```

Output:

```text
[nan]
```

## Theory

### The simple version

Many forecasting features say "what was the value one step ago?". Shifting the series by one position gives that feature for every row, and the very first row has nothing to look back on.

### The definition

$$\text{lag}_t=\begin{cases}\text{NaN}&t=0\\ x_{t-1}&t\ge1\end{cases}$$

### Why it matters

- Forecasting models often use "what was the value one step ago?" as a feature.
- The first row has no past, and marking it NaN (not 0) says so honestly.

### How it works

1. Create an output of the same length.
2. Put NaN in the first position.
3. Copy the series shifted right by one.

### Worked example

For $(10,20,30,40)$ each value moves one place to the right and the first slot has nothing to hold, so the result is [nan, 10.0, 20.0, 30.0].

## Explanation

The result is the input shifted right by one with a `NaN` placed at the front. Using `NaN` rather than `0` is deliberate: `0` would be a real, misleading value, while `NaN` is clearly "unknown" and is handled explicitly by downstream imputation.
