---
name: problem-27-z-score-scaling
title: 'Z-Score Scaling'
tags: [problemset, data-stats-for-ds, data-cleaning]
difficulty: Beginner
kind: problemset
relatedModule: 'part-data-science|Data Processing'
topic: 'data cleaning'
hint: 'subtract the column mean, divide by the column std, guard a zero std'
tools: [NumPy]
---

## Statement

Standardize each feature (column) to zero mean and unit variance using the population standard deviation.

Implement `solve(X)`.

**Returns.** Return a NumPy array of the same shape. A constant column has zero spread, so it maps to all zeros.

### Examples

**Example 1**

Input:

```python
solve([[1.0], [2.0], [3.0]])
```

Output:

```text
[[-1.224745], [0.0], [1.224745]]
```

**Example 2**

Input:

```python
solve([[4.0], [4.0]])
```

Output:

```text
[[0.0], [0.0]]
```

## Theory

### The simple version

Z-scores measure how many standard deviations each value is from the column mean. After standardizing, every feature has mean 0 and standard deviation 1.

### The formula

$$z=\frac{x-\mu}{\sigma},\qquad \sigma=\sqrt{\frac1n\sum_i (x_i-\mu)^2}$$

## Explanation

The standard deviation uses divisor $n$ (population), which matches the common library scalers. A zero standard deviation would divide by zero, so such columns return zeros.
