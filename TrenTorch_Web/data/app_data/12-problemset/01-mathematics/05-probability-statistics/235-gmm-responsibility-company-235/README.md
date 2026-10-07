---
name: gmm-responsibility-company-235
title: 'gmm-responsibility — PhonePe case'
tags: [problemset, unsupervised-ml, gaussian-mixture-models, phonepe]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'PhonePe'
hint: 'log(pi) - log(sigma) - 0.5*((x-mu)/sigma)^2, subtract the max, exponentiate, normalise'
tools: [NumPy]
---

## Statement

PhonePe-inspired transaction segmentation model represents each observation with a mixture of Gaussian components. You need to calculate the component responsibility so the team can update assignments during the next EM iteration.

Compute the responsibilities of a one-dimensional Gaussian mixture for the scalar observation `x`. `mu`, `sigma` and `pi` are arrays holding each component's mean, standard deviation and mixing weight. The posterior is computed in log space, so observations far from every component stay finite.

Implement `solve(x, mu, sigma, pi)`.

**Returns.** Return a NumPy vector with one probability per component that sums to 1.

### Examples

**Example 1**

Input:

```python
solve(0.0, [0.0, 4.0], [1.0, 1.0], [0.5, 0.5])
```

Output:

```text
[0.999665, 0.000335]
```

**Example 2**

Input:

```python
solve(1.0, [0.0, 2.0], [1.0, 1.0], [0.8, 0.2])
```

Output:

```text
[0.8, 0.2]
```

**Example 3**

Input:

```python
solve(100.0, [0.0, 10.0], [1.0, 1.0], [0.5, 0.5])
```

Output:

```text
[0.0, 1.0]
```

## Theory

### The simple version

A Gaussian mixture explains the data as coming from several bell curves. For one observation, Bayes' rule says how likely each curve is to be its source: the component's prior weight times how well it explains the point, normalised over all components. This is the E-step of the EM algorithm.

### The formula

$$r_k=\frac{\pi_k\,\mathcal N(x\mid\mu_k,\sigma_k^2)}{\sum_j\pi_j\,\mathcal N(x\mid\mu_j,\sigma_j^2)}\;\propto\;\frac{\pi_k}{\sigma_k}\,e^{-\frac12\left(\frac{x-\mu_k}{\sigma_k}\right)^2}$$

## Explanation

The factor $1/\sqrt{2\pi}$ is common to all components and cancels. Working with logarithms and subtracting the largest log-score avoids $0/0$ when the observation is so far from every component that all densities underflow; the third example is $100$ away from both means and still returns valid probabilities, with all the mass on the nearer component.
