---
name: problem-34-welch-t-statistic
title: 'Welch t Statistic'
tags: [problemset, data-stats-for-ds, hypothesis-testing]
difficulty: Advanced
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'hypothesis testing'
hint: 'difference of means over sqrt(var_a/n_a + var_b/n_b), with ddof=1'
tools: [NumPy]
---

## Statement

Compute Welch's t-statistic for two independent samples that may have different sizes and different variances. Use the unbiased sample variance (divide by $n-1$).

Implement `solve(a, b)`.

**Returns.** Return the statistic as a Python float. Each sample needs at least two values so that its variance exists.

### Examples

**Example 1**

Input:

```python
solve([5.0, 6.0, 7.0, 8.0], [1.0, 2.0, 3.0, 5.0])
```

Output:

```text
3.503245
```

**Example 2**

Input:

```python
solve([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
```

Output:

```text
0.0
```

## Theory

### The simple version

The t-statistic says how many standard errors apart the two sample means are. Welch's version does not pretend the two groups share one variance: each group contributes its own variance divided by its own size.

### The formula

$$t=\frac{\bar a-\bar b}{\sqrt{\dfrac{s_a^2}{n_a}+\dfrac{s_b^2}{n_b}}},\qquad s^2=\frac1{n-1}\sum_i (x_i-\bar x)^2$$

### Why it matters

- Welch's t compares two means without assuming the groups have equal variance or size, which is rarely true in practice.
- It says how many standard errors apart the means are, which is what significance depends on.

### How it works

1. Compute each sample's mean and unbiased variance ($n-1$).
2. Standard error: $\sqrt{s_a^2/n_a+s_b^2/n_b}$.
3. $t=(\bar a-\bar b)/\text{SE}$.

### Worked example

Sample $a=(5,6,7,8)$ has mean $6.5$ and variance $1.667$; sample $b=(1,2,3,5)$ has mean $2.75$ and variance $2.917$. The standard error is $\sqrt{1.667/4+2.917/4}=\sqrt{1.146}=1.0705$, so $t=3.75/1.0705=3.503245$.

## Explanation

The denominator is the standard error of the difference of means. With `ddof=1` the variances are the unbiased sample variances. Identical samples give a numerator of $0$ and therefore $t=0$.
