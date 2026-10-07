---
name: problem-16-monte-carlo-expectation
title: 'Monte Carlo Expectation'
tags: [problemset, maths-stats-for-ml, probability]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability'
topic: 'probability'
hint: 'apply f to the samples, then take the mean'
tools: [NumPy]
---

## Statement

Estimate the expectation $\mathbb E[f(X)]$ from samples of $X$ by averaging $f$ over the samples.

Implement `solve(f, samples)`.

**Returns.** Return a float. An empty sample gives `nan`.

### Examples

**Example 1**

Input:

```python
solve(lambda s: s**2, [1.0, 2.0, 3.0])
```

Output:

```text
4.666667
```

**Example 2**

Input:

```python
solve(lambda s: s, [0.0, 10.0])
```

Output:

```text
5.0
```

## Theory

### The simple version

Monte Carlo estimation replaces an average over all possible outcomes with an average over a handful of random draws. The more draws, the closer the average gets to the true expected value.

### The formula

$$\mathbb E[f(X)]\approx\frac1N\sum_{i=1}^{N}f(x_i)$$

The error shrinks like $1/\sqrt N$.

## Explanation

The function `f` is called once on the whole array of samples, so it should work element-wise on NumPy arrays. The mean of the results is the estimate.
