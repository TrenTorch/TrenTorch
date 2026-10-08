---
name: problem-23-mean-imputation
title: 'Mean Imputation'
tags: [problemset, data-stats-for-ds, data-cleaning]
difficulty: Advanced
kind: problemset
relatedModule: 'part-data-science|Data Processing'
topic: 'data cleaning'
hint: 'compute the mean ignoring NaN, then fill the gaps'
tools: [NumPy]
---

## Statement

Replace the missing (`NaN`) entries of a numeric vector with the mean of the observed entries.

Implement `solve(x)`.

**Returns.** Return a new NumPy array; the input is not modified.

### Examples

**Example 1**

Input:

```python
solve([1.0, np.nan, 3.0])
```

Output:

```text
[1.0, 2.0, 3.0]
```

**Example 2**

Input:

```python
solve([np.nan, 4.0, 6.0, np.nan])
```

Output:

```text
[5.0, 4.0, 6.0, 5.0]
```

## Theory

### The simple version

Mean imputation fills each gap with the average of the values you do have, so the column's mean stays the same.

### The formula

$$\tilde x_i=\begin{cases}x_i & x_i\text{ observed}\\[2pt] \bar x_{\text{obs}} & x_i\text{ missing}\end{cases},\qquad \bar x_{\text{obs}}=\frac1{|O|}\sum_{i\in O}x_i$$

### Why it matters

- Most models cannot accept missing values.
- Filling gaps with the mean is the simplest imputation and keeps the column mean unchanged.

### How it works

1. Compute the mean of the observed (non-NaN) entries.
2. Replace every NaN with that mean.

### Worked example

For $(1,\text{NaN},3)$ the observed entries are $1$ and $3$ with mean $2$, so the gap becomes $2$: [1.0, 2.0, 3.0].

## Explanation

`np.nanmean` ignores the missing entries when computing the fill value, and the work happens on a copy. If every entry is missing there is nothing to average, and the result stays `NaN`.
