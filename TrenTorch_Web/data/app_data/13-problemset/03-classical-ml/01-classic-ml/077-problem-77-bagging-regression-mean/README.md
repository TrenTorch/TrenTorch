---
name: problem-77-bagging-regression-mean
title: 'Bagging Regression Mean'
tags: [problemset, classical-ml-trees-ensembles, bagging]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'bagging'
hint: 'mean over the model axis'
tools: [NumPy]
---

## Statement

Average the predictions of several regressors (for example trees trained on bootstrap samples). `predictions` has shape `(n_models, n_samples)`.

Implement `solve(predictions)`.

**Returns.** Return a NumPy array of length `n_samples` holding the mean prediction of the models for each sample. For a 1-D input the result is a single float.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 2.0], [3.0, 4.0], [5.0, 9.0]])
```

Output:

```text
[3.0, 5.0]
```

**Example 2**

Input:

```python
solve([1.0, 2.0, 3.0])
```

Output:

```text
2.0
```

## Theory

### The simple version

Bagging reduces variance. Each model is trained on a different bootstrap sample, so their errors differ; averaging many of them cancels much of the noise while leaving the shared signal.

### The formula

$$\hat f(x)=\frac1B\sum_{b=1}^{B}\hat f_b(x)$$

### Why it matters

- Averaging many regressors reduces variance without increasing bias.
- It is the regression counterpart of the forest's vote.

### How it works

1. Stack the predictions with one row per model.
2. Average over the models.

### Worked example

For models $(1,2)$, $(3,4)$, $(5,9)$ the first sample averages $(1+3+5)/3=3$ and the second $(2+4+9)/3=5$, so [3.0, 5.0].

## Explanation

The average is taken over the model axis (axis 0), one value per sample. If the $B$ models' errors have variance $\sigma^2$ and are uncorrelated, the average has variance $\sigma^2/B$; correlation between models limits the gain.
