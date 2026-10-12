---
name: problem-41-winsorize-values
title: 'Winsorize Values'
tags: [problemset, data-stats-for-ds, eda]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-data-science|Data Processing'
topic: 'EDA'
hint: 'np.quantile for the two cut-offs, then np.clip'
tools: [NumPy]
---

## Statement

Winsorize a numeric vector: compute its `lower` and `upper` quantiles (defaults $0.05$ and $0.95$) and clip every value to that range. Extreme values are pulled in to the cut-offs instead of being removed.

Implement `solve(x, lower=0.05, upper=0.95)`.

**Returns.** Return a NumPy array of the same length. Quantiles use NumPy's default linear interpolation.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0, 4.0, 100.0], 0.2, 0.8)
```

Output:

```text
[1.8, 2.0, 3.0, 4.0, 23.2]
```

**Example 2**

Input:

```python
solve([5.0, 5.0, 5.0])
```

Output:

```text
[5.0, 5.0, 5.0]
```

## Theory

### The simple version

Outliers can dominate means and regression fits. Winsorizing keeps the data points but caps how extreme they are: anything below the 5th percentile becomes the 5th percentile, and anything above the 95th becomes the 95th.

### The formula

$$y_i=\min\!\big(\max(x_i,\,q_{\text{lower}}),\,q_{\text{upper}}\big)$$

### Why it matters

- Extreme values can dominate means, regressions and scaling, but deleting rows breaks alignment with other columns.
- Winsorising keeps every row and only limits how extreme a value can be.

### How it works

1. Compute the lower and upper quantiles of the data.
2. Clip every value to that range.

### Worked example

For $(1,2,3,4,100)$ with quantiles $0.2$ and $0.8$: the $0.2$ quantile sits $0.8$ of the way from $1$ to $2$, so it is $1.8$; the $0.8$ quantile is $4+0.2\cdot96=23.2$. The $1$ is raised to $1.8$ and the $100$ is cut to $23.2$, giving [1.8, 2.0, 3.0, 4.0, 23.2].

## Explanation

Only the extreme tails change; the middle of the data is untouched. Unlike deleting outliers, winsorizing keeps the sample size, which is useful when rows must stay aligned with other columns.
