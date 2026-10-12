---
name: problem-24-median-imputation
title: 'Median Imputation'
tags: [problemset, data-stats-for-ds, data-cleaning]
difficulty: Advanced
kind: problemset
relatedModule: 'part-data-science|Data Processing'
topic: 'data cleaning'
hint: 'compute the median ignoring NaN, then fill the gaps'
tools: [NumPy]
---

## Statement

Replace the missing (`NaN`) entries of a numeric vector with the median of the observed entries.

Implement `solve(x)`.

**Returns.** Return a new NumPy array; the input is not modified.

### Examples

**Example 1**

Input:

```python
solve([1.0, np.nan, 3.0, 100.0])
```

Output:

```text
[1.0, 3.0, 3.0, 100.0]
```

**Example 2**

Input:

```python
solve([2.0, 4.0, np.nan, 10.0])
```

Output:

```text
[2.0, 4.0, 4.0, 10.0]
```

## Theory

### The simple version

The median is the middle value, so a single huge outlier barely moves it. That makes median imputation a safer default than the mean when the data has extreme values.

### The formula

$$\tilde x_i=\operatorname{median}\{x_j: x_j\text{ observed}\}\quad\text{for each missing }i$$

### Why it matters

- The median is not pulled around by outliers, so it is a safer fill value than the mean for skewed data.
- It keeps imputed values realistic when a few extreme values exist.

### How it works

1. Take the observed (non-NaN) entries.
2. Compute their median.
3. Replace every NaN with it.

### Worked example

For $(1,\text{NaN},3,100)$ the observed values $1,3,100$ have median $3$, so the gap becomes $3$ and the result is [1.0, 3.0, 3.0, 100.0]. The mean would have been $34.7$, dominated by the outlier $100$.

## Explanation

`np.nanmedian` ignores the missing entries, and the fill happens on a copy. In the first example the mean of the observed values would be about $34.7$, dragged up by the outlier $100$, while the median $3$ stays with the bulk of the data.
