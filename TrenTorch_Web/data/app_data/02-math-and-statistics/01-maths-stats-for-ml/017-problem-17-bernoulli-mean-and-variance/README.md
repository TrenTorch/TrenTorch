---
name: problem-17-bernoulli-mean-and-variance
title: "Bernoulli Mean and Variance"
tags: [problemset, maths-stats-for-ml, probability]
difficulty: Intermediate
kind: problemset
relatedModule: "part-math|Probability"
topic: "probability"
hint: "use p̂ and p̂(1-p̂)"
tools: [NumPy]
---

# Bernoulli Mean and Variance

## Statement

Implement `solve(x)`. Return the empirical mean and Bernoulli variance of a sequence of binary observations.

## Theory

For Bernoulli data, the sample mean estimates p and the variance is p(1-p).

## Explanation

Evaluate the specified sample or feature operation and return the result in the documented form. Inputs are passed directly to `solve`; no input parsing or printing is required.

## Examples

**Example 1**

Input:
```python
solve([0, 1, 1, 0, 1])
```

Output:
```text
(0.6, 0.24)
```

**Example 2**

Input:
```python
solve([1, 1, 1, 1])
```

Output:
```text
(1.0, 0.0)
```
