---
name: research-scaling-fit-exponent
title: 'Scaling Laws: Fitting the Exponent'
tags: [research-papers, transformers, llm, scaling]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Given measured losses at several model sizes, a power law can be fitted by a straight-line regression in log-log space. The slope of that line is minus the exponent, which tells you how fast returns to scale diminish.

### From theory to code

Implement `fit_power_law_exponent(N, L)`, returning the exponent `alpha` from a least-squares line through `log N` and `log L`.

### Constraints

- Returns a Python float.

### Hints

<details>
<summary>Hint 1</summary>

Use `np.polyfit` on the logs with degree 1, then return the negative of the slope.

</details>

## Theory

### The simple version

Taking logs turns the power law into a line, so ordinary linear regression recovers its parameters. The negated slope is the exponent.

### The formula

$$\log L = \log c - \alpha \log N \quad\Longrightarrow\quad \alpha = -\text{slope}$$

### How NumPy/PyTorch actually implements this

`np.polyfit(np.log(N), np.log(L), 1)` returns the slope and intercept directly.

## Explanation

The fit is ordinary least squares on log-transformed data, the same procedure the paper uses to estimate the exponents.
