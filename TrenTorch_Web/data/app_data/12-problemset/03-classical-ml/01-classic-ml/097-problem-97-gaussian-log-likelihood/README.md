---
name: problem-97-gaussian-log-likelihood
title: 'Gaussian Log Likelihood'
tags: [problemset, unsupervised-ml, gaussian-mixture]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'gaussian mixture'
hint: '-0.5 * (d*log(2*pi) + logdet(cov) + (x-mu)^T cov^-1 (x-mu))'
tools: [NumPy]
---

## Statement

Compute the log-density of a multivariate normal distribution $\mathcal N(\mu,\Sigma)$ at one point `x`. The covariance matrix is symmetric positive definite.

Implement `solve(x,mu,cov)`.

**Returns.** Return the log-density as a Python float.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0], [0.0, 0.0], [[1.0, 0.0], [0.0, 1.0]])
```

Output:

```text
-4.337877
```

**Example 2**

Input:

```python
solve([0.0], [0.0], [[4.0]])
```

Output:

```text
-1.612086
```

## Theory

### The simple version

The log-density says how plausible a point is under a Gaussian: it is highest at the mean and falls off with the squared Mahalanobis distance, which is distance measured in units of the covariance. Working with logs avoids tiny numbers that underflow.

### The formula

$$\log\mathcal N(x\mid\mu,\Sigma)=-\tfrac12\Big(d\log2\pi+\log|\Sigma|+(x-\mu)^\top\Sigma^{-1}(x-\mu)\Big)$$

## Explanation

The log-determinant comes from `slogdet`, which is stable, and the quadratic form is computed with a linear solve instead of an explicit inverse. For the standard 2-D normal at $(1,2)$ the quadratic term is $5$, giving $-\tfrac12(2\log2\pi+5)\approx-4.34$.
