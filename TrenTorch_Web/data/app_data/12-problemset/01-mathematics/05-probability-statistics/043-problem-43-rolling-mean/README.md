---
name: problem-43-rolling-mean
title: 'Rolling Mean'
tags: [problemset, data-stats-for-ds, time-series]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'time series'
hint: 'keep a running sum: add the new value, subtract the one leaving the window'
tools: [NumPy]
---

## Statement

Compute the trailing rolling mean of width `window`: position $i$ holds the mean of the last `window` values ending at $i$. The first `window - 1` positions do not have a full window yet.

Implement `solve(x, window)`.

**Returns.** Return a float NumPy array the same length as `x`, with `NaN` in the first `window - 1` positions. `window` must be at least 1 (otherwise `ValueError`); a window longer than `x` gives all `NaN`.

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
solve([2.0, 4.0, 6.0, 8.0, 10.0], 3)
```

Output:

```text
[nan, nan, 4.0, 6.0, 8.0]
```

## Theory

### The simple version

A rolling mean smooths noise: each point is replaced by the average of itself and the few points before it. Computing every window from scratch costs $O(nw)$, but adjacent windows overlap almost completely.

### The trick

Keep a running sum. Moving the window one step to the right adds the new value and subtracts the one that fell out, so each output costs $O(1)$:

$$S_i=S_{i-1}+x_i-x_{i-w},\qquad \text{mean}_i=S_i/w$$

### Why it matters

- Rolling means smooth noise in time series and are a basic feature for forecasting.
- A running sum makes each output $O(1)$ instead of recomputing the whole window.

### How it works

1. Keep a running sum of the values added so far.
2. Once the window is full, subtract the value that just left it.
3. Divide the sum by the window size; earlier positions stay NaN.

### Worked example

With window $2$ on $(1,2,3,4)$: position 0 has no full window (NaN), then $(1+2)/2=1.5$, $(2+3)/2=2.5$ and $(3+4)/2=3.5$, so [nan, 1.5, 2.5, 3.5].

## Explanation

The running sum makes the whole pass linear in the length of the series. Only positions with a complete window get a value; the earlier ones stay `NaN` instead of using a shorter partial window.
