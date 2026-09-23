---
name: potd-rollout-check-two-proportion-z
title: 'THE ROLLOUT CHECK'
tags: [probability-and-statistics]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Probability & Statistics

---

### Story

Robinhood A/B-tests a new order-ticket UI against the existing one. Before anyone calls the
difference "real," it needs a proper two-proportion z-test, not just eyeballing two percentages.

---

### The Math

```
p_hat = (x1 + x2) / (n1 + n2)
SE = sqrt( p_hat * (1 - p_hat) * (1/n1 + 1/n2) )
z = (p2 - p1) / SE
```

Two-sided p-value from the standard normal CDF, where `p1 = x1/n1` and `p2 = x2/n2` (group 1 =
control, group 2 = treatment).

### Input Format

```
n1 x1 n2 x2
```

### Output Format

`p1 p2 z pvalue`, 6 decimals.

### Constraints

- `1 <= n1, n2 <= 10^7`, `0 <= x_i <= n_i`
- Time limit: 1.0 second.

---

### Example

**Input**

```
5000 250 5000 300
```

**Output**

```
0.050000 0.060000 2.193172 0.028295
```

## Theory

### The simple version

An A/B test's two proportions look different on the surface, but this test asks whether that difference is bigger than you would expect from random noise alone, given how much data you have.

### The pooled proportion, not the average of the two

`p_hat` (used inside the standard error) is the pooled conversion rate across both groups combined
`(x1+x2)/(n1+n2)`, not the simple average of `p1` and `p2`. The two only coincide when `n1 = n2`.

### The zero-variance collapse

If `x1 = x2 = 0`, `p_hat = 0` and `SE = 0`, making `z` undefined by division. The convention: report
`z = 0.000000` and `pvalue = 1.000000`, meaning no evidence of a difference when there is no
variance in the data at all to measure a difference against. Identical conversion rates
(`p1 = p2` exactly, even with nonzero data) give the same `z = 0`, `pvalue = 1` result, this time
through the ordinary formula rather than a special case, since the numerator `p2 - p1` is `0`.

### A fixed, documented normal CDF

The p-value comes from the standard normal CDF, `Phi`. Any consistent, documented approximation
(this problem uses the `erf`-based closed form) is acceptable as long as every implementation is
compared against the same one, since different CDF approximations can differ in the last couple of
decimal places.

## Explanation

`two_proportion_z_test` computes `p1`, `p2`, and the pooled `p_hat` directly, then `SE` from the
pooled rate. If `SE` is exactly `0`, it sets `z = 0.0` directly rather than dividing; otherwise
`z = (p2 - p1) / SE`. The p-value is `2 * (1 - Phi(|z|))` with
`Phi(t) = 0.5 * (1 + erf(t / sqrt(2)))`. Because `Phi(0) = 0.5` exactly, `z = 0` (whether from the
explicit zero-variance branch or from `p1 == p2` flowing through the ordinary formula) always gives
`pvalue = 2 * (1 - 0.5) = 1.0`, so the "no evidence of a difference" answer falls out of the same
p-value formula both ways.
