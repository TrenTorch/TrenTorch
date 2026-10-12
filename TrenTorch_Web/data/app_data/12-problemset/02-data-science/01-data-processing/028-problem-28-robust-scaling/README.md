---
name: problem-28-robust-scaling
title: 'Robust Scaling'
tags: [problemset, data-stats-for-ds, data-cleaning]
difficulty: Beginner
kind: problemset
relatedModule: 'part-data-science|Data Processing'
topic: 'data cleaning'
hint: 'subtract the median, divide by Q3 minus Q1'
tools: [NumPy]
---

## Statement

Scale each feature (column) by centering it at its median and dividing by its interquartile range $Q_3-Q_1$ (quartiles use linear interpolation).

Implement `solve(X)`.

**Returns.** Return a NumPy array of the same shape. A column whose interquartile range is zero maps to all zeros.

### Examples

**Example 1**

Input:

```python
solve([[1.0], [2.0], [3.0], [4.0]])
```

Output:

```text
[[-1.0], [-0.333333], [0.333333], [1.0]]
```

**Example 2**

Input:

```python
solve([[0.0], [0.0], [0.0], [9.0]])
```

Output:

```text
[[0.0], [0.0], [0.0], [4.0]]
```

## Theory

### The simple version

Robust scaling uses the median and the middle $50\%$ of the data instead of the mean and standard deviation, so a few extreme values do not distort the scale.

### The formula

$$x'=\frac{x-\operatorname{median}(x)}{Q_3(x)-Q_1(x)}$$

### Why it matters

- The mean and standard deviation are dragged around by outliers; the median and interquartile range are not.
- Robust scaling keeps the bulk of the data well scaled even when extreme values exist.

### How it works

1. For each column find the median and the quartiles $Q_1,Q_3$.
2. Map $x\mapsto(x-\text{median})/(Q_3-Q_1)$.
3. A column with zero interquartile range maps to zeros.

### Worked example

For $(1,2,3,4)$: median $2.5$, $Q_1=1.75$, $Q_3=3.25$, so the IQR is $1.5$. The values become $(1-2.5)/1.5=-1$, $-1/3$, $1/3$ and $1$, giving [[-1.0], [-0.333333], [0.333333], [1.0]].

## Explanation

The second example has one large outlier: the interquartile range ignores it, so the other values stay near zero. Columns with zero spread map to zeros rather than dividing by zero.
