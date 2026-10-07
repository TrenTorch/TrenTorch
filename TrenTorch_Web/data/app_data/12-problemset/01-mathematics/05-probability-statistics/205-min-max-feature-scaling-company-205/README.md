---
name: min-max-feature-scaling-company-205
title: 'min-max-feature-scaling — AWS case'
tags: [problemset, data-stats-for-ds, data-cleaning, aws]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'AWS'
hint: '(x - min) / (max - min), zeros when max == min'
tools: [NumPy]
---

## Statement

AWS-inspired monitoring model combines numeric signals that arrive on very different scales. Before training, the team needs every feature mapped to a fixed interval, so you need to implement min-max scaling and handle the stated boundary cases correctly.

Map the values linearly so the minimum becomes 0 and the maximum becomes 1. If all values are equal (the range is zero) return all zeros.

Implement `solve(x)`.

**Returns.** Return a float NumPy vector in $[0,1]$.

### Examples

**Example 1**

Input:

```python
solve([10.0, 20.0, 30.0])
```

Output:

```text
[0.0, 0.5, 1.0]
```

**Example 2**

Input:

```python
solve([5.0, 5.0, 5.0])
```

Output:

```text
[0.0, 0.0, 0.0]
```

**Example 3**

Input:

```python
solve([-1.0, 0.0, 3.0])
```

Output:

```text
[0.0, 0.25, 1.0]
```

## Theory

### The simple version

Features measured on very different scales (dollars versus clicks) distort distance-based and gradient-based models. Min-max scaling squeezes every feature into the same $[0,1]$ range while preserving the ordering and the relative spacing of the values.

### The formula

$$x'=\frac{x-x_{\min}}{x_{\max}-x_{\min}}$$

## Explanation

The minimum maps to $0$, the maximum to $1$ and everything else falls proportionally in between (the midpoint $20$ maps to $0.5$). A constant feature would divide by zero, so it is mapped to zeros. A single extreme outlier compresses all other values towards one end, which is the method's main weakness.
