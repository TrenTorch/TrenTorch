---
name: problem-16-monte-carlo-expectation
title: 'Monte Carlo Expectation'
tags: [problemset, maths-stats-for-ml, probability]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability'
topic: 'probability'
hint: 'average the transformed samples'
tools: [NumPy]
---

## Statement

Implement `solve(f, samples)`. Estimate E[f(X)] from observed samples by averaging the function values. The callable f must accept a NumPy array of samples.

### Examples

**Example 1**

Input:

```python
solve(lambda x: x**2, [1.0, 2.0, 3.0])
```

Output:

```text
4.666666666666667
```

**Example 2**

Input:

```python
solve(lambda x: x, [2.0, 4.0, 6.0])
```

Output:

```text
4.0
```

## Theory

The empirical expectation is the sample average of f evaluated at each observed value.

## Explanation

Evaluate the specified sample or feature operation and return the result in the documented form. Inputs are passed directly to `solve`; no input parsing or printing is required.
