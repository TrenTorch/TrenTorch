---
name: problem-32-bootstrap-mean
title: 'Bootstrap Mean'
tags: [problemset, data-stats-for-ds, sampling]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability'
topic: 'sampling'
hint: 'resample with replacement B times, take the alpha/2 and 1-alpha/2 quantiles of the means'
tools: [NumPy]
---

## Statement

Estimate a percentile bootstrap confidence interval for the mean of a sample. Draw `B` resamples of the same size with replacement using `np.random.default_rng(seed)`, take each resample's mean, and return the `alpha/2` and `1 - alpha/2` quantiles of those means.

Implement `solve(x, B=1000, alpha=0.05, seed=0)`.

**Returns.** Return a tuple `(low, high)` of Python floats. Quantiles use NumPy's default linear interpolation.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0, 4.0])
```

Output:

```text
(1.5, 3.5)
```

**Example 2**

Input:

```python
solve([5.0, 5.0, 5.0])
```

Output:

```text
(5.0, 5.0)
```

**Example 3**

Input:

```python
solve([1.0, 2.0, 3.0, 4.0, 10.0], B=500, alpha=0.1, seed=7)
```

Output:

```text
(2.0, 6.8)
```

## Theory

### The simple version

We only have one sample, but we want to know how much its mean would wobble if we could collect the data again. The bootstrap fakes "collecting again" by resampling the data we have, with replacement, many times. The spread of the resampled means approximates the spread of the real sampling distribution.

### The recipe

1. Draw $B$ resamples $x^{*(1)},\dots,x^{*(B)}$, each of size $n$, with replacement.
2. Compute $\bar x^{*(b)}$ for each.
3. The $(1-\alpha)$ percentile interval is $[\,q_{\alpha/2},\;q_{1-\alpha/2}\,]$ of those $B$ means.

### Why it matters

- The bootstrap estimates uncertainty from a single sample without assuming a distribution.
- It works for statistics with no simple formula, not just the mean.

### How it works

1. Draw $B$ resamples of the data with replacement.
2. Compute the mean of each resample.
3. Take the $\alpha/2$ and $1-\alpha/2$ quantiles of those means.

### Worked example

For $(1,2,3,4)$ the resampled means range between $1$ and $4$ and are centred at $2.5$. Using 1000 resamples and the 2.5% and 97.5% quantiles gives the interval (1.5, 3.5).

## Explanation

A constant sample always resamples to itself, so its interval collapses to a single point. The result depends on the random generator, which is why the seed is part of the contract: with the same seed the same resamples are drawn in the same order.
