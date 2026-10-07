---
name: problem-35-confidence-interval-for-mean
title: 'Confidence Interval for Mean'
tags: [problemset, data-stats-for-ds, confidence-intervals]
difficulty: Advanced
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'confidence intervals'
hint: 'mean plus/minus critical times std(ddof=1)/sqrt(n)'
tools: [NumPy]
---

## Statement

Build a normal-approximation confidence interval for the mean of a sample: $\bar x\pm z\cdot s/\sqrt n$ with the unbiased standard deviation $s$ and a critical value `critical` (default $1.96$, i.e. 95%).

Implement `solve(x, critical=1.96)`.

**Returns.** Return a tuple `(low, high)`. The sample needs at least two values so that $s$ exists.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0, 4.0])
```

Output:

```text
(1.234825, 3.765175)
```

**Example 2**

Input:

```python
solve([10.0, 12.0, 11.0, 13.0, 9.0], critical=2.576)
```

Output:

```text
(9.178493, 12.821507)
```

## Theory

### The simple version

The sample mean is only an estimate. The standard error $s/\sqrt n$ says how much it typically wobbles, and multiplying it by $1.96$ gives a range that covers the true mean about 95% of the time, if the sample mean is roughly normally distributed.

### The formula

$$\bar x\pm z\,\frac{s}{\sqrt n},\qquad s=\sqrt{\frac1{n-1}\sum_i (x_i-\bar x)^2}$$

## Explanation

The interval is centred on the sample mean and its half-width grows with the spread of the data and shrinks with $\sqrt n$. Passing `critical=2.576` gives a 99% interval. For very small samples a t critical value would be more accurate than the normal one.
