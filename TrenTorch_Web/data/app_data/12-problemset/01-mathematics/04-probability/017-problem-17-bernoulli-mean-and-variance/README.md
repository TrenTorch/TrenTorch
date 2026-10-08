---
name: problem-17-bernoulli-mean-and-variance
title: 'Bernoulli Mean and Variance'
tags: [problemset, maths-stats-for-ml, probability]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability'
topic: 'probability'
hint: 'the variance of a Bernoulli variable is p times (1 minus p)'
tools: [NumPy]
---

## Statement

Compute the empirical mean and variance of binary (0/1) observations.

Implement `solve(x)`.

**Returns.** Return a tuple `(mean, variance)` of floats, where the variance is $\hat p(1-\hat p)$. Empty input, non-binary values or a non-1-D input raise `ValueError`.

### Examples

**Example 1**

Input:

```python
solve([1, 0, 1, 1])
```

Output:

```text
(0.75, 0.1875)
```

**Example 2**

Input:

```python
solve([0, 0, 0])
```

Output:

```text
(0.0, 0.0)
```

## Theory

### The simple version

A Bernoulli variable is a coin flip that is 1 with probability $p$. Its mean is $p$ and its variance is $p(1-p)$, which is largest for a fair coin and zero for a coin that never changes.

### The formula

$$\hat p=\frac1n\sum_i x_i,\qquad \widehat{\operatorname{Var}}=\hat p(1-\hat p)$$

### Why it matters

- A yes/no outcome (click, convert, fail) is a Bernoulli variable, and its mean and variance are the two numbers every A/B analysis starts from.
- The variance depends only on the mean, so one number describes the whole spread.

### How it works

1. The mean is the fraction of ones, $\hat p$.
2. The variance is $\hat p(1-\hat p)$.

### Worked example

For observations $1,0,1,1$: three of four are ones, so $\hat p=0.75$ and the variance is $0.75\cdot0.25=0.1875$, giving (0.75, 0.1875).

## Explanation

The variance is the plug-in value $\hat p(1-\hat p)$, which equals the population variance (no $n-1$ correction). Empty input has no mean, so it raises `ValueError`, as does any value other than 0 or 1.
