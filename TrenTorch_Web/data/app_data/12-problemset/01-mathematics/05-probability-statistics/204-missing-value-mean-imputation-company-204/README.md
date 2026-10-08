---
name: missing-value-mean-imputation-company-204
title: 'missing-value-mean-imputation — Microsoft case'
tags: [problemset, data-stats-for-ds, data-cleaning, microsoft]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Microsoft'
hint: 'per column: nanmean, then fill NaNs with it'
tools: [NumPy]
---

## Statement

This is a hypothetical engineering scenario inspired by the kind of work a **Microsoft** ranking and experimentation team might handle; it is not a real interview question or a claim that Microsoft uses this exact task. The team needs a reliable implementation for feature cleaning in a production-oriented ML workflow. A small implementation error can change the model input or metric enough to make a downstream result misleading.

Replace NaN entries in each feature column with that column's mean computed from the observed values.

Process each column independently: compute the mean of its observed (non-NaN) values and put it in place of every `NaN` in that column. A column with no observed value stays `NaN`.

Implement `solve(X)`.

**Returns.** Return a new float NumPy matrix of the same shape. The input is not modified.

Process each column independently: compute the mean of its observed (non-NaN) values and put it in place of every `NaN` in that column. A column with no observed value stays `NaN`.

Implement `solve(X)`.

**Returns.** Return a new float NumPy matrix of the same shape. The input is not modified.

### Examples

**Example 1**

Input:

```python
solve([[1.0, float('nan')], [3.0, 5.0]])
```

Output:

```text
[[1.0, 5.0], [3.0, 5.0]]
```

**Example 2**

Input:

```python
solve([[1.0, 2.0], [float('nan'), 4.0], [5.0, float('nan')]])
```

Output:

```text
[[1.0, 2.0], [3.0, 4.0], [5.0, 3.0]]
```

## Theory

### The simple version

Most models cannot handle missing values. Mean imputation is the simplest remedy: replace each gap with the average of that feature. It keeps the column mean unchanged, but it shrinks the variance and ignores relationships between features.

### The formula

$$\tilde x_{ij}=\begin{cases}x_{ij}&x_{ij}\text{ observed}\\\bar x_j^{\,\text{obs}}&x_{ij}=\text{NaN}\end{cases}$$

### Why it matters

- Most models cannot accept missing values.
- Mean imputation is the simplest fix and keeps the column mean unchanged, at the cost of shrinking the variance.

### How it works

1. For each column compute the mean of the observed (non-NaN) entries.
2. Replace every NaN in that column with it.

### Worked example

The second column has the single observed value $5$, so its mean is $5$ and the missing entry becomes $5$. The first column has no gaps: [[1.0, 5.0], [3.0, 5.0]].

## Explanation

`np.nanmean` skips missing entries when averaging a column, so the mean is not poisoned by the `NaN`s. Always compute the means on the training data only and reuse them for new data to avoid leakage.
