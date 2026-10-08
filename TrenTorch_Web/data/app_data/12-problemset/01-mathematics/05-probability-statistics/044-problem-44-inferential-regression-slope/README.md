---
name: problem-44-inferential-regression-slope
title: 'Inferential Regression Slope'
tags: [problemset, data-stats-for-ds, regression-for-inference]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'regression for inference'
hint: 'slope = covariance sum over x variance sum; intercept = mean_y - slope*mean_x'
tools: [NumPy]
---

## Statement

Fit a straight line $y=\text{slope}\cdot x+\text{intercept}$ to paired data by ordinary least squares. `x` and `y` must have the same length.

Implement `solve(x,y)`.

**Returns.** Return a tuple `(slope, intercept)` of floats. A different length raises `ValueError`. If all `x` values are equal the slope is undefined.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0], [2.0, 4.0, 5.0])
```

Output:

```text
(1.5, 0.666667)
```

**Example 2**

Input:

```python
solve([0.0, 1.0, 2.0, 3.0], [1.0, 3.0, 5.0, 7.0])
```

Output:

```text
(2.0, 1.0)
```

## Theory

### The simple version

Least squares picks the line that makes the sum of squared vertical gaps to the data as small as possible. For one predictor the answer has a closed form: the slope is how much $x$ and $y$ vary together divided by how much $x$ varies on its own, and the line always passes through the point of means.

### The formulas

$$\hat\beta_1=\frac{\sum_i (x_i-\bar x)(y_i-\bar y)}{\sum_i (x_i-\bar x)^2},\qquad \hat\beta_0=\bar y-\hat\beta_1\bar x$$

### Why it matters

- A line fit is the simplest model of how one quantity depends on another, and its slope is the effect you report.
- The closed form shows exactly how least squares works before moving to many features.

### How it works

1. Compute the means $\bar x$ and $\bar y$.
2. Slope $=\sum(x-\bar x)(y-\bar y)/\sum(x-\bar x)^2$.
3. Intercept $=\bar y-\text{slope}\cdot\bar x$.

### Worked example

For $x=(1,2,3)$ and $y=(2,4,5)$: $\bar x=2$, $\bar y=3.667$. The cross sum is $(-1)(-1.667)+0+(1)(1.333)=3$ and $\sum(x-\bar x)^2=2$, so the slope is $1.5$ and the intercept is $3.667-1.5\cdot2=0.667$, which is (1.5, 0.666667).

## Explanation

The slope is computed first from the centred sums, and the intercept follows from the requirement that the fitted line passes through $(\bar x,\bar y)$. Perfectly linear data, as in the second example, is recovered exactly.
