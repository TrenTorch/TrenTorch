---
name: agentic-success-rate-confidence-interval
title: Success Rate & Confidence Intervals
tags: [agentic-systems, evaluation, statistics, benchmarks]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The headline number for an agent on a benchmark is its **success rate**: tasks solved divided by tasks attempted. But a rate from 20 tasks is far less trustworthy than one from 2,000, and comparing "62% versus 58%" without error bars is how teams fool themselves. A **confidence interval** shows the uncertainty. The simple normal approximation misbehaves for small samples and for rates near 0 or 1 (it can produce intervals outside `[0, 1]`). The **Wilson score interval** fixes this and is the standard recommendation for proportions.

### From theory to code

Implement `success_rate` and `wilson_interval`.

### Constraints

- `success_rate(successes, n)` returns `successes / n` (`0.0` when `n == 0`).
- `wilson_interval(successes, n, z=1.96)` returns `(low, high)`: with `p = successes / n`, centre `(p + z**2 / (2n)) / (1 + z**2 / n)` and half-width `z * sqrt(p(1 - p)/n + z**2 / (4n**2)) / (1 + z**2 / n)`; the interval is `centre -+ half-width`.
- For `n == 0` return `(0.0, 1.0)`: no data means no information.

### Hints

<details>
<summary>Hint 1</summary>

Clamp the bounds to `[0, 1]`: the interval is never outside it, even for `successes = 0` or `n`, but floating-point rounding can leave a bound a hair outside.

</details>

<details>
<summary>Hint 2</summary>

Doubling `n` while keeping `p` fixed shrinks the interval by roughly `sqrt(2)`.

</details>

## Theory

### The simple version

A restaurant with one review saying "great" is not five stars, and with 2,000 reviews averaging 4.6 it nearly is. The interval is the honest range of what the true quality could be.

### The formula

$$
\tilde p = \frac{p + \tfrac{z^2}{2n}}{1 + \tfrac{z^2}{n}}, \qquad
\text{half} = \frac{z}{1 + \tfrac{z^2}{n}}\sqrt{\frac{p(1 - p)}{n} + \frac{z^2}{4n^2}}
$$

### How this is done in practice

Statsmodels' `proportion_confint(method='wilson')` computes this. Benchmark papers increasingly report intervals, and comparing two agents requires either non-overlap, which is conservative, or a paired test on the same tasks.

## Explanation

A closed-form expression with a safe definition for the empty case. The tests check the properties that make Wilson preferable to the naive formula: it stays inside `[0, 1]` and is informative even at 0% or 100%.
