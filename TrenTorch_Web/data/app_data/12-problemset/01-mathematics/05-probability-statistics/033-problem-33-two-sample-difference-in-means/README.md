---
name: problem-33-two-sample-difference-in-means
title: 'Two-Sample Difference in Means'
tags: [problemset, data-stats-for-ds, hypothesis-testing]
difficulty: Advanced
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'hypothesis testing'
hint: 'mean of a minus mean of b, each over its own length'
tools: [NumPy]
---

## Statement

Compute the observed difference between the means of two samples, $\bar a-\bar b$. The samples may have different lengths.

Implement `solve(a, b)`.

**Returns.** Return the difference as a Python float (positive when `a` has the larger mean).

### Examples

**Example 1**

Input:

```python
solve([5.0, 6.0, 7.0], [1.0, 2.0, 3.0])
```

Output:

```text
4.0
```

**Example 2**

Input:

```python
solve([1.0, 2.0], [3.0, 4.0, 5.0, 6.0])
```

Output:

```text
-3.0
```

## Theory

### The simple version

Most A/B-style comparisons start with the simplest possible summary: how far apart are the two group averages? Every test statistic (t, z, permutation) is built from this raw difference.

### The formula

$$\Delta=\bar a-\bar b=\frac1{n_a}\sum_i a_i-\frac1{n_b}\sum_j b_j$$

## Explanation

Each mean is computed over its own sample size, so unequal group sizes need no special handling. The sign matters: swapping the arguments flips the sign of the result.
