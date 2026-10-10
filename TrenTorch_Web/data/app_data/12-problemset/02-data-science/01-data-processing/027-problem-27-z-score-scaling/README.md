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

### Why it matters

- Many algorithms assume features centred at zero with a similar spread, and standardisation provides it.
- A z-score reads as "how many standard deviations from the mean", which makes features directly comparable.

### How it works

1. For each column compute the mean and the population standard deviation.
2. Map $x\mapsto(x-\mu)/\sigma$.
3. A constant column maps to zeros.

### Worked example

For $(1,2,3)$ the mean is $2$ and $\sigma=\sqrt{2/3}\approx0.8165$, so the values become $-1/0.8165$, $0$ and $1/0.8165$, which is [[-1.224745], [0.0], [1.224745]].

## Explanation

The standard deviation uses divisor $n$ (population), which matches the common library scalers. A zero standard deviation would divide by zero, so such columns return zeros.
