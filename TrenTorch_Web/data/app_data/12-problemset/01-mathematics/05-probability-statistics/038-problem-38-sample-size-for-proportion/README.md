---
name: problem-38-sample-size-for-proportion
title: 'Sample Size for Proportion'
tags: [problemset, data-stats-for-ds, experiment-design]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'experiment design'
hint: '((1.96*sqrt(2 pbar (1-pbar)) + 0.84*sqrt(p1(1-p1)+p2(1-p2)))^2) / (p1-p2)^2, rounded up'
tools: [NumPy]
---

## Statement

Estimate the sample size needed **per group** to detect a difference between two proportions $p_1$ and $p_2$ with a two-sided test, using $z_{\alpha/2}=1.96$ (5% significance) and $z_\beta=0.84$ (80% power).

Implement `solve(p1, p2)`.

**Returns.** Return an `int`, rounded up. Both rates must lie in $[0,1]$ and must differ; otherwise `ValueError` is raised.

### Examples

**Example 1**

Input:

```python
solve(0.1, 0.15)
```

Output:

```text
685
```

**Example 2**

Input:

```python
solve(0.5, 0.6)
```

Output:

```text
387
```

## Theory

### The simple version

The smaller the difference you want to detect, the more users you need. The formula balances two risks: falsely declaring a difference (significance) and missing a real one (power).

### The formula

With $\bar p=(p_1+p_2)/2$:

$$n=\left\lceil\frac{\left(z_{\alpha/2}\sqrt{2\bar p(1-\bar p)}+z_\beta\sqrt{p_1(1-p_1)+p_2(1-p_2)}\right)^2}{(p_1-p_2)^2}\right\rceil$$

### Why it matters

- Running a test with too few users cannot reliably detect a real effect, and too many wastes time.
- Planning the sample size in advance fixes the false-alarm rate and the power before the data arrive.

### How it works

1. Take $z_{\alpha/2}=1.96$ and $z_\beta=0.84$.
2. Pool the rates: $\bar p=(p_1+p_2)/2$.
3. Combine the two standard deviations, square, divide by $(p_1-p_2)^2$ and round up.

### Worked example

For $p_1=0.1$ and $p_2=0.15$: $\bar p=0.125$, $1.96\sqrt{2\cdot0.125\cdot0.875}=0.9167$ and $0.84\sqrt{0.09+0.1275}=0.3918$. Their sum $1.3085$ squared is $1.7121$, divided by $0.05^2=0.0025$ gives $684.8$, which rounds up to 685.

## Explanation

The first term in the bracket covers the null hypothesis (variance under a shared rate $\bar p$), the second covers the alternative (each group's own variance). The squared difference in the denominator is why halving the detectable effect roughly quadruples the sample size.
