---
name: problem-21-map-bernoulli-estimate
title: 'MAP Bernoulli Estimate'
tags: [problemset, maths-stats-for-ml, bayesian-inference]
difficulty: Advanced
kind: problemset
relatedModule: 'part-mathematics|Probability'
topic: 'Bayesian inference'
hint: 'add prior pseudo-counts to successes and failures'
tools: [NumPy]
---

## Statement

Implement `solve(x, a, b)`. Return the posterior mode for a Bernoulli probability with a Beta(a,b) prior, using the observed binary values.

### Examples

**Example 1**

Input:

```python
solve([1, 1, 0, 1], 1.0, 1.0)
```

Output:

```text
0.75
```

**Example 2**

Input:

```python
solve([1, 1, 0], 2.0, 2.0)
```

Output:

```text
0.6
```

## Theory

The Beta posterior parameters are a+successes and b+failures; its mode is (a_post−1)/(a_post+b_post−2).

## Explanation

Evaluate the specified sample or feature operation and return the result in the documented form. Inputs are passed directly to `solve`; no input parsing or printing is required.
