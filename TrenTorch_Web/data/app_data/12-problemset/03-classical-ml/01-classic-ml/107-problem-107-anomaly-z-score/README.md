---
name: problem-107-anomaly-z-score
title: 'Anomaly Z-Score'
tags: [problemset, unsupervised-ml, anomaly-detection]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'anomaly detection'
hint: '|x - mean| / std > threshold, with z = 0 where std = 0'
tools: [NumPy]
---

## Statement

Flag anomalies by z-score. Standardise `x` with its mean and **population** standard deviation (column-wise for a 2-D array) and mark every entry whose absolute z-score is strictly greater than `threshold` (default $3$). A constant column has z-score $0$ everywhere.

Implement `solve(x, threshold=3)`.

**Returns.** Return a boolean NumPy array of the same shape as `x`.

### Examples

**Example 1**

Input:

```python
solve([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 50.0], 2.5)
```

Output:

```text
[False, False, False, False, False, False, False, False, False, True]
```

**Example 2**

Input:

```python
solve([[1.0, 5.0], [2.0, 5.0], [3.0, 5.0]], 1.0)
```

Output:

```text
[[True, False], [False, False], [True, False]]
```

## Theory

### The simple version

A z-score says how many standard deviations a value is from the mean. Values far out in the tails, typically beyond $3$, are unusual enough to be treated as anomalies. It is the simplest outlier detector and works best for roughly bell-shaped data.

### The formula

$$z_i=\frac{x_i-\mu}{\sigma},\qquad \text{anomaly}\iff |z_i|>\tau$$

### Why it matters

- A z-score flags values unusually far from the mean, the simplest anomaly detector.
- It assumes roughly bell-shaped data.

### How it works

1. Compute the mean and population standard deviation.
2. $z=(x-\mu)/\sigma$.
3. Flag $|z|>$ threshold.

### Worked example

Nine values equal $1$ and one equals $50$: the mean is $5.9$ and $\sigma=14.7$. The $50$ has $z=(50-5.9)/14.7=3.0>2.5$ and the others have $|z|=0.33$, so the result is [False, False, False, False, False, False, False, False, False, True].

## Explanation

A single large outlier inflates $\sigma$ itself, so with few samples its z-score cannot grow without bound (for $n$ points it is at most $\sqrt{n-1}$), which is why the first example uses a threshold of $2.5$ rather than $3$. Constant columns have $\sigma=0$; setting their z-score to $0$ avoids dividing by zero and flags nothing.
