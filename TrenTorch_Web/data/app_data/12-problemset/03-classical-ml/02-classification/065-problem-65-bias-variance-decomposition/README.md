---
name: problem-65-bias-variance-decomposition
title: 'Bias-Variance Decomposition'
tags: [problemset, classical-ml, bias-variance]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'bias variance'
hint: 'mean_pred = predictions.mean(axis=0); bias2 = mean((mean_pred-y)^2); var = mean of per-column variance'
tools: [NumPy]
---

## Statement

Estimate the bias and variance of a model from the predictions of several models (for example trained on different bootstrap samples) on the same observations. `predictions` has shape `(n_models, n_observations)` and `y` holds the true targets.

Implement `solve(predictions, y)`.

**Returns.** Return a tuple `(squared_bias, variance)`. Squared bias is the mean over observations of $(\bar f(x)-y)^2$, where $\bar f$ is the average prediction across models. Variance is the mean over observations of the (population, `ddof=0`) variance of the predictions across models.

### Examples

**Example 1**

Input:

```python
solve([[2, 4], [4, 6]], [3, 5])
```

Output:

```text
(0.0, 1.0)
```

**Example 2**

Input:

```python
solve([[1.0, 2.0], [1.0, 2.0], [1.0, 2.0]], [0.0, 0.0])
```

Output:

```text
(2.5, 0.0)
```

## Theory

### The simple version

Prediction error has two sources. _Bias_ is being consistently wrong in the same direction (the average of many models misses the truth). _Variance_ is being inconsistent (different training sets give different answers). Flexible models usually trade lower bias for higher variance.

### The formulas

$$\text{bias}^2=\frac1m\sum_{j}\big(\bar f_j-y_j\big)^2,\qquad \text{var}=\frac1m\sum_{j}\frac1B\sum_{b}\big(f_{b,j}-\bar f_j\big)^2$$

## Explanation

In the first example the two models average to exactly the targets, so the bias is $0$, but they disagree by $\pm1$ around that average, giving variance $1$. In the second all models agree (variance $0$) but are consistently off, so all the error is bias.
