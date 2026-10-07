---
name: problem-26-min-max-scaling
title: 'Min-Max Scaling'
tags: [problemset, data-stats-for-ds, data-cleaning]
difficulty: Beginner
kind: problemset
relatedModule: 'part-data-science|Data Processing'
topic: 'data cleaning'
hint: 'subtract the column minimum, divide by the range, guard a zero range'
tools: [NumPy]
---

## Statement

Scale each feature (column) of a matrix into $[0, 1]$ using that column's minimum and maximum.

Implement `solve(X)`.

**Returns.** Return a NumPy array of the same shape. A constant column has no range, so it maps to all zeros.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]])
```

Output:

```text
[[0.0, 0.0], [0.5, 0.5], [1.0, 1.0]]
```

**Example 2**

Input:

```python
solve([[5.0], [5.0]])
```

Output:

```text
[[0.0], [0.0]]
```

## Theory

### The simple version

Min-max scaling squeezes each feature into the same $[0, 1]$ range so that features measured in different units contribute comparably.

### The formula

$$x'=\frac{x-x_{\min}}{x_{\max}-x_{\min}}$$

## Explanation

Minimum and maximum are taken per column. When they are equal the division would be $0/0$, so those columns are filled with zeros instead of NaN.
