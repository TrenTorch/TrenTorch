---
name: problem-20-mle-of-gaussian-mean
title: "MLE of Gaussian Mean"
tags: [problemset, maths-stats-for-ml, estimation]
difficulty: Intermediate
kind: problemset
relatedModule: "part-data-foundations|Probability & Statistics"
topic: "estimation"
hint: "the MLE is the sample mean"
tools: [NumPy]
---

# MLE of Gaussian Mean

## Statement

Implement `solve(x)`. Return the maximum-likelihood estimate of the mean of Gaussian observations.

## Theory

For a Gaussian model with unknown mean, the likelihood is maximized at the arithmetic sample mean.

## Explanation

Evaluate the specified sample or feature operation and return the result in the documented form. Inputs are passed directly to `solve`; no input parsing or printing is required.

## Examples

**Example 1**

Input:
```python
solve([1.0, 2.0, 3.0])
```

Output:
```text
2.0
```

**Example 2**

Input:
```python
solve([-2.0, 4.0])
```

Output:
```text
1.0
```
