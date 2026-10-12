---
name: problem-37-pooled-proportion-test-statistic
title: 'Pooled Proportion Test Statistic'
tags: [problemset, data-stats-for-ds, ab-testing]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'ab testing'
hint: 'pool all outcomes for the standard error: p(1-p)(1/n_a + 1/n_b)'
tools: [NumPy]
---

## Statement

Compute the pooled two-proportion z-statistic for two groups of 0/1 outcomes under the null hypothesis that both groups have the same underlying rate.

Implement `solve(a, b)`.

**Returns.** Return the z-statistic as a Python float, positive when `a` has the higher rate. If every outcome in both groups is identical the pooled variance is zero and the statistic is not finite.

### Examples

**Example 1**

Input:

```python
solve([1, 1, 0, 1, 0, 0, 1, 1], [0, 0, 1, 0, 0, 1, 0, 0])
```

Output:

```text
1.511858
```

**Example 2**

Input:

```python
solve([1, 0, 1, 0], [1, 0, 1, 0])
```

Output:

```text
0.0
```

## Theory

### The simple version

If the two groups really share one rate, the best estimate of that rate uses everyone's data together (the pooled rate). The z-statistic then asks how many standard errors apart the observed group rates are, assuming that single shared rate.

### The formula

$$\hat p=\frac{\sum a+\sum b}{n_a+n_b},\qquad z=\frac{\hat p_a-\hat p_b}{\sqrt{\hat p(1-\hat p)\left(\frac1{n_a}+\frac1{n_b}\right)}}$$

### Why it matters

- To test whether two conversion rates differ, we need the standard error under the null hypothesis that they are the same.
- Under the null the best estimate of the shared rate pools both groups.

### How it works

1. Pool: $\hat p=(\sum a+\sum b)/(n_a+n_b)$.
2. Standard error: $\sqrt{\hat p(1-\hat p)(1/n_a+1/n_b)}$.
3. $z=(\hat p_a-\hat p_b)/\text{SE}$.

### Worked example

Group $a$ has $5$ ones in $8$ ($0.625$) and group $b$ has $2$ in $8$ ($0.25$). The pooled rate is $7/16=0.4375$, the standard error is $\sqrt{0.4375\cdot0.5625\cdot0.25}=0.248$, and $z=0.375/0.248=1.511858$.

## Explanation

The pooled rate $\hat p$ is computed once from all observations and used in the standard error, which is the form that is valid under the null hypothesis. Equal rates give $z=0$.
