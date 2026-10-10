---
name: problem-29-iqr-outlier-flagging
title: 'IQR Outlier Flagging'
tags: [problemset, data-stats-for-ds, eda]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-data-science|Data Processing'
topic: 'EDA'
hint: 'compute Q1, Q3 and the two fences, then compare'
tools: [NumPy]
---

## Statement

Flag observations that lie more than $1.5$ interquartile ranges below the first quartile or above the third quartile (Tukey's fences).

Implement `solve(x)`.

**Returns.** Return a boolean NumPy array, `True` where a value is an outlier.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0, 4.0, 100.0])
```

Output:

```text
[False, False, False, False, True]
```

**Example 2**

Input:

```python
solve([1.0, 2.0, 3.0])
```

Output:

```text
[False, False, False]
```

## Theory

### The simple version

Tukey's rule marks a point as unusual if it falls well outside the box that holds the middle half of the data.

### The formula

$$x\text{ is an outlier}\iff x<Q_1-1.5\,\mathrm{IQR}\ \text{ or }\ x>Q_3+1.5\,\mathrm{IQR},\qquad \mathrm{IQR}=Q_3-Q_1$$

### Why it matters

- Outliers can dominate means, regressions and scaling, so spotting them is the first data-cleaning step.
- Tukey's fences use quartiles, so a few extreme values cannot hide themselves by inflating the spread.

### How it works

1. Compute $Q_1$, $Q_3$ and $\text{IQR}=Q_3-Q_1$.
2. Set the fences $Q_1-1.5\,\text{IQR}$ and $Q_3+1.5\,\text{IQR}$.
3. Flag every value outside the fences.

### Worked example

For $(1,2,3,4,100)$: $Q_1=2$, $Q_3=4$, IQR $=2$, so the fences are $2-3=-1$ and $4+3=7$. Only $100$ lies outside, giving [False, False, False, False, True].

## Explanation

Quartiles use linear interpolation. A value exactly on a fence is not flagged, because the comparisons are strict.
