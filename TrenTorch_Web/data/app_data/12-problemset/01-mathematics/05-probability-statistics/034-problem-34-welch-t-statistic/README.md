---
name: problem-34-welch-t-statistic
title: 'Welch t Statistic'
tags: [problemset, data-stats-for-ds, hypothesis-testing]
difficulty: Advanced
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'hypothesis testing'
hint: 'use unequal-variance standard error'
tools: [NumPy]
---

## Statement

Implement `solve(a, b)`. Compute Welch’s t-statistic comparing the means of two independent samples with unequal variances.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0], [2.0, 3.0, 4.0])
```

Output:

```text
-1.224744871391589
```

**Example 2**

Input:

```python
solve([2.0, 4.0, 6.0], [1.0, 2.0, 3.0])
```

Output:

```text
1.5491933384829668
```

## Theory

Welch’s statistic divides the difference in sample means by the standard error computed from each sample variance and sample size.

## Explanation

The output is computed from the supplied observations using the method above. Values and arrays are passed directly as arguments; the function returns its result without printing.
