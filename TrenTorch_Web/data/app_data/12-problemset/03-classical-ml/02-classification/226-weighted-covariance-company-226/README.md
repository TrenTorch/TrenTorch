---
name: weighted-covariance-company-226
title: 'weighted-covariance — CRED case'
tags: [problemset, maths-stats-for-ml, probability-foundations, cred]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'Classification'
caseCompany: 'CRED'
hint: 'p = w / w.sum(); mu = p @ X; Z = X - mu; (Z * p[:, None]).T @ Z'
tools: [NumPy]
---

## Statement

CRED-inspired risk analytics pipeline assigns different importance to observations based on their reliability. You need to compute the weighted covariance so the downstream model captures the relationship between features using those observation weights.

Normalise the weights to sum to 1 ($p_i=w_i/\sum w$), compute the weighted mean $\mu=\sum_ip_ix_i$ and return $\Sigma=\sum_ip_i(x_i-\mu)(x_i-\mu)^\top$. No small-sample bias correction is applied.

Implement `solve(X, w)`.

**Returns.** Return a symmetric $d\times d$ float NumPy matrix. The weights must be non-negative and not all zero.

Normalise the weights to sum to 1 ($p_i=w_i/\sum w$), compute the weighted mean $\mu=\sum_ip_ix_i$ and return $\Sigma=\sum_ip_i(x_i-\mu)(x_i-\mu)^\top$. No small-sample bias correction is applied.

Implement `solve(X, w)`.

**Returns.** Return a symmetric $d\times d$ float NumPy matrix. The weights must be non-negative and not all zero.

### Examples

**Example 1**

Input:

```python
solve([[1, 2], [3, 4], [5, 1]], [1, 2, 1])
```

Output:

```text
[[2.0, -0.5], [-0.5, 1.6875]]
```

**Example 2**

Input:

```python
solve([[1.0, 0.0], [3.0, 2.0]], [1.0, 1.0])
```

Output:

```text
[[1.0, 1.0], [1.0, 1.0]]
```

## Theory

### The simple version

An ordinary covariance treats every observation as equally trustworthy. When some observations are more reliable than others, each one is given a weight, and both the mean and the spread are computed with those weights. Heavily weighted points then pull the mean toward themselves and dominate the spread.

### The formulas

$$p_i=\frac{w_i}{\sum_jw_j},\qquad \mu=\sum_ip_ix_i,\qquad \Sigma=\sum_ip_i\,(x_i-\mu)(x_i-\mu)^\top$$

### Why it matters

- Some observations are more reliable than others and should count for more.
- Weighting changes both the mean and the spread, so both must use the same weights.

### How it works

1. Divide the weights by their sum.
2. Compute the weighted mean.
3. Sum the weighted outer products of the centred rows.

### Worked example

The weights $(1,2,1)$ become $(0.25,0.5,0.25)$ and the weighted mean is $(3,\,2.75)$. The centred rows are $(-2,-0.75)$, $(0,1.25)$ and $(2,-1.75)$, giving variances $2$ and $1.6875$ and covariance $-0.5$: [[2.0, -0.5], [-0.5, 1.6875]].

## Explanation

The weighted mean is subtracted first, then each centred outer product is weighted by $p_i$. With equal weights this is the _population_ covariance (divide by $n$, not $n-1$): the second example gives the matrix of all ones. In the first example the weights $(1,2,1)$ give the middle point half of the total weight.
