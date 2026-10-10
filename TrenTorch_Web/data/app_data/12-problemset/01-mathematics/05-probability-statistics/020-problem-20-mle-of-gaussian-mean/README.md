---
name: problem-20-mle-of-gaussian-mean
title: 'MLE of Gaussian Mean'
tags: [problemset, maths-stats-for-ml, estimation]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'estimation'
hint: 'the maximum-likelihood mean is the sample average'
tools: [NumPy]
---

## Statement

Return the maximum-likelihood estimate of the mean of a Gaussian distribution from its samples.

Implement `solve(x)`.

**Returns.** Return a float. An empty sample gives `nan`.

### Examples

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
solve([-1.0, 1.0])
```

Output:

```text
0.0
```

## Theory

### The simple version

Maximum likelihood picks the parameter that makes the observed data most probable. For a Gaussian, the best-fitting mean is simply the sample average.

### The formula

Setting the derivative of the log-likelihood to zero gives $\sum_i (x_i-\mu)=0$, so

$$\hat\mu=\frac1n\sum_{i=1}^{n}x_i$$

### Why it matters

- Maximum likelihood chooses the parameter that makes the observed data most probable, and it is the principle behind most training losses.
- For a Gaussian with known variance, the answer is simply the sample mean.

### How it works

1. Write the log-likelihood of the samples under $\mathcal N(\mu,\sigma^2)$.
2. Set its derivative with respect to $\mu$ to zero.
3. Solving gives $\hat\mu=\frac1n\sum x_i$.

### Worked example

For samples $1,2,3$ the sum is $6$ and $6/3=2.0$.

## Explanation

The answer does not depend on the variance, because the variance is a separate parameter and the mean's condition decouples from it. The function is the arithmetic mean of the samples.
