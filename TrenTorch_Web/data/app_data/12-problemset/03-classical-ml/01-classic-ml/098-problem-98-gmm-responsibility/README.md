---
name: problem-98-gmm-responsibility
title: 'GMM Responsibility'
tags: [problemset, unsupervised-ml, gaussian-mixture]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'gaussian mixture'
hint: 'log weight + log pdf per component, subtract the max, exponentiate, normalise'
tools: [NumPy]
---

## Statement

Compute the responsibilities of a Gaussian mixture model for one point `x`: the posterior probability that each component generated it. `weights` are the mixture weights, `means` the component means and `covs` the covariance matrices.

Implement `solve(x, weights, means, covs)`.

**Returns.** Return a NumPy vector of length `K` that sums to 1.

### Examples

**Example 1**

Input:

```python
solve([0.0], [0.5, 0.5], [[0.0], [4.0]], [[[1.0]], [[1.0]]])
```

Output:

```text
[0.999665, 0.000335]
```

**Example 2**

Input:

```python
solve([1.0], [0.8, 0.2], [[0.0], [2.0]], [[[1.0]], [[1.0]]])
```

Output:

```text
[0.8, 0.2]
```

## Theory

### The simple version

A Gaussian mixture says each point came from one of $K$ bell curves, but we do not know which. Bayes' rule turns the prior (mixture weight) and the likelihood (how well the component explains the point) into the probability that each component is responsible. This is the E-step of the EM algorithm.

### The formula

$$r_k=\frac{\pi_k\,\mathcal N(x\mid\mu_k,\Sigma_k)}{\sum_j\pi_j\,\mathcal N(x\mid\mu_j,\Sigma_j)}$$

### Why it matters

- Responsibilities say how much each Gaussian explains a point, which drives the E-step of EM.
- Using logs avoids $0/0$ when the point is far from every component.

### How it works

1. For each component compute $\log\pi_k+\log\mathcal N(x\mid\mu_k,\Sigma_k)$.
2. Subtract the largest value and exponentiate.
3. Normalise to sum to $1$.

### Worked example

The point $0$ is at the mean of component 0 and $4$ away from component 1, so the densities have ratio $e^{-8}=0.000335$. With equal weights the responsibilities are $1/(1+0.000335)=0.999665$ and $0.000335$: [0.999665, 0.000335].

## Explanation

The computation is done in log space and the largest log-score is subtracted before exponentiating (log-sum-exp trick), so far-away points do not underflow to $0/0$. In the first example the point sits at the mean of component 0, which therefore takes almost all the responsibility.
