---
name: problem-103-explained-variance-ratio
title: 'Explained Variance Ratio'
tags: [problemset, unsupervised-ml, pca]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'pca'
hint: 'eigenvalues divided by their sum (zeros if the sum is 0)'
tools: [NumPy]
---

## Statement

Convert the eigenvalues of a covariance matrix into explained-variance ratios: each eigenvalue divided by their sum.

Implement `solve(eigenvalues)`.

**Returns.** Return a NumPy vector that sums to 1. If the eigenvalues sum to zero, return a vector of zeros.

### Examples

**Example 1**

Input:

```python
solve([2.0, 1.0])
```

Output:

```text
[0.666667, 0.333333]
```

**Example 2**

Input:

```python
solve([5.0, 3.0, 2.0])
```

Output:

```text
[0.5, 0.3, 0.2]
```

**Example 3**

Input:

```python
solve([0.0, 0.0])
```

Output:

```text
[0.0, 0.0]
```

## Theory

### The simple version

Each eigenvalue of the covariance matrix is the variance along one principal direction, so the total variance is their sum. Dividing each one by the total gives the fraction of the data's variance that component explains. Summing the largest few shows how many components you need to keep.

### The formula

$$\text{EVR}_i=\frac{\lambda_i}{\sum_j\lambda_j}$$

## Explanation

In the second example the first component explains $50\%$ of the variance and the first two together $80\%$. A zero total (all-constant data) would divide by zero, so zeros are returned instead.
