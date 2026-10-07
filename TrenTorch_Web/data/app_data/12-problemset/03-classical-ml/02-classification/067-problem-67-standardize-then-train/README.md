---
name: problem-67-standardize-then-train
title: 'Standardize Then Train'
tags: [problemset, classical-ml, feature-engineering]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'feature engineering'
hint: 'subtract the column mean, divide by the column std (use 1 where std is 0)'
tools: [NumPy]
---

## Statement

Standardise every column of a training matrix: subtract the column mean and divide by the column **population** standard deviation (`ddof=0`). A constant column maps to zeros. Only the supplied matrix is used, so no information from a test set can leak in.

Implement `solve(x)`.

**Returns.** Return a float NumPy array with the same shape as `x`, where each non-constant column has mean $0$ and standard deviation $1$.

### Examples

**Example 1**

Input:

```python
solve([[1, 10], [3, 14], [5, 18]])
```

Output:

```text
[[-1.224745, -1.224745], [0.0, 0.0], [1.224745, 1.224745]]
```

**Example 2**

Input:

```python
solve([[2, 7], [2, 9]])
```

Output:

```text
[[0.0, -1.0], [0.0, 1.0]]
```

## Theory

### The simple version

Features on very different scales (age in years, income in dollars) confuse many algorithms. Standardising gives every feature a mean of 0 and a spread of 1 so that none dominates simply because of its units.

### The formula

$$z_{ij}=\frac{x_{ij}-\mu_j}{\sigma_j}$$

where $\mu_j,\sigma_j$ are the mean and standard deviation of column $j$.

## Explanation

A constant column has $\sigma=0$, which would divide by zero; replacing that standard deviation by $1$ turns the column into zeros instead. In real pipelines $\mu$ and $\sigma$ must be computed on the training set only and then re-used for validation and test data.
