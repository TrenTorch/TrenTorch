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

### Why it matters

- Many expectations have no closed form, so we average the function over random samples instead.
- By the law of large numbers the average converges to the true expectation, with error shrinking like $1/\sqrt n$.

### How it works

1. Evaluate $f$ on each sample.
2. Average the results.

### Worked example

For $f(s)=s^2$ and samples $1,2,3$: the values are $1,4,9$, their sum is $14$, and $14/3=4.666667$.

## Explanation

The function `f` is called once on the whole array of samples, so it should work element-wise on NumPy arrays. The mean of the results is the estimate.
