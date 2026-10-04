---
name: problem-32-bootstrap-mean
title: "Bootstrap Mean"
tags: [problemset, data-stats-for-ds, sampling]
difficulty: Intermediate
kind: problemset
relatedModule: "part-math|Probability"
topic: "sampling"
hint: "resample rows with replacement and collect means"
tools: [NumPy]
---

# Bootstrap Mean

## Statement

Implement `solve(x, B=1000, alpha=0.05, seed=0)`. Estimate a percentile confidence interval for the sample mean using B bootstrap resamples, confidence tail probability alpha, and random seed.

## Theory

Each bootstrap replicate samples n observations with replacement and computes its mean; the interval is given by the alpha/2 and 1−alpha/2 quantiles.

## Explanation

The output is computed from the supplied observations using the method above. Values and arrays are passed directly as arguments; the function returns its result without printing.

## Examples

**Example 1**

Input:
```python
solve([2.0, 2.0, 2.0], B=100, seed=4)
```

Output:
```text
(2.0, 2.0)
```

**Example 2**

Input:
```python
solve([0.0, 0.0, 0.0], B=100, seed=4)
```

Output:
```text
(0.0, 0.0)
```
