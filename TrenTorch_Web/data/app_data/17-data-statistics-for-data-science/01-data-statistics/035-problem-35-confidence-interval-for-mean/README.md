---
name: problem-35-confidence-interval-for-mean
title: "Confidence Interval for Mean"
tags: [problemset, data-stats-for-ds, confidence-intervals]
difficulty: Advanced
kind: problemset
relatedModule: "part-data-foundations|Probability & Statistics"
topic: "confidence intervals"
hint: "mean ± critical_value*SE"
tools: [NumPy]
---

# Confidence Interval for Mean

## Statement

Implement `solve(x, critical=1.96)`. Return a normal-approximation confidence interval for the mean using the sample standard deviation and supplied critical value.

## Theory

The standard error is s/√n; the interval is x̄ ± critical·SE.

## Explanation

The output is computed from the supplied observations using the method above. Values and arrays are passed directly as arguments; the function returns its result without printing.

## Examples

**Example 1**

Input:
```python
solve([1.0, 2.0, 3.0])
```

Output:
```text
(0.8683934723883333, 3.131606527611667)
```

**Example 2**

Input:
```python
solve([5.0, 5.0, 5.0], critical=2.0)
```

Output:
```text
(5.0, 5.0)
```
