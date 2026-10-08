---
name: problem-21-map-bernoulli-estimate
title: 'MAP Bernoulli Estimate'
tags: [problemset, maths-stats-for-ml, bayesian-inference]
difficulty: Advanced
kind: problemset
relatedModule: 'part-mathematics|Probability'
topic: 'Bayesian inference'
hint: 'add the observed counts to the Beta parameters, then take the mode'
tools: [NumPy]
---

## Statement

Compute the maximum a posteriori (MAP) estimate of a Bernoulli probability under a Beta$(a, b)$ prior, given 0/1 observations.

Implement `solve(x, a, b)`.

**Returns.** Return a float. The posterior mode is only interior when both posterior parameters exceed 1; use $a, b \ge 1$. Observations must be 0/1 and $a,b\ge1$, otherwise `ValueError` is raised; with $a=b=1$ and no observations every value is equally likely, so that case raises `ValueError` too.

### Examples

**Example 1**

Input:

```python
solve([1, 1, 0, 1], 2.0, 2.0)
```

Output:

```text
0.666667
```

**Example 2**

Input:

```python
solve([0, 0], 2.0, 2.0)
```

Output:

```text
0.25
```

## Theory

### The simple version

A Beta prior acts like extra imaginary coin flips added to the real ones. The MAP estimate is the most probable value of the coin's bias after combining the prior with the data.

### The formula

With $k$ successes in $n$ trials the posterior is Beta$(a+k,\;b+n-k)$, whose mode is

$$\hat p_{\text{MAP}}=\frac{a+k-1}{a+b+n-2}$$

For $a=b=1$ (a uniform prior) this equals the plain frequency $k/n$.

### Why it matters

- MAP estimation adds a prior to maximum likelihood, which stabilises estimates when data are scarce.
- With a Beta prior it behaves like adding imaginary extra coin flips, and it is the Bayesian reading of regularisation.

### How it works

1. Count the successes $k$ and the trials $n$.
2. The posterior is Beta$(a+k,\;b+n-k)$.
3. Return its mode $(a+k-1)/(a+b+n-2)$.

### Worked example

For observations $1,1,0,1$ ($k=3$, $n=4$) and prior $a=b=2$: the posterior is Beta$(5,3)$, and its mode is $(5-1)/(5+3-2)=4/6=0.666667$. Without the prior the estimate would be $0.75$.

## Explanation

The reference forms the two posterior parameters and returns the mode of the Beta distribution. With few data points the prior pulls the estimate toward $0.5$, as the second example shows.
