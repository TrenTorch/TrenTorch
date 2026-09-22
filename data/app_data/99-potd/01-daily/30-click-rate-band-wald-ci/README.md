---
name: potd-click-rate-band-wald-ci
title: 'THE CLICK-RATE BAND'
tags: [probability-and-statistics]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Probability & Statistics

---

### Story

A search-ads team reports today's click-through rate to stakeholders every morning, and a bare
point estimate without an uncertainty band has burned them before on low-traffic days.

---

### The Math

```
p_hat = clicks / n
SE = sqrt( p_hat * (1 - p_hat) / n )
interval = p_hat +- z * SE,   z = 1.959964   (95% interval)
```

### Input Format

```
n clicks
```

### Output Format

`p_hat lower upper`, 6 decimals.

### Constraints

- `1 <= clicks <= n <= 10^9`
- Time limit: 1.0 second.

---

### Example

**Input**

```
1000 45
```

**Output**

```
0.045000 0.032151 0.057849
```

## Theory

### The simple version

A single point estimate like "4.5% click rate" hides how much you should trust it. A confidence interval wraps a range around that estimate that gets wider the less data you have backing it up.

### The z-value is fixed, not computed

`z = 1.959964` for a 95% interval is a fixed constant here, not a runtime call to a stats library's
inverse normal CDF. Fixing it exactly means every implementation, in any language, lands on the same
answer within the grading tolerance, regardless of which library (or hand-rolled approximation) it
would otherwise use.

### The collapse at 0 and 1

When `clicks = 0`, `p_hat = 0` and `SE = 0`, so the interval collapses to `(0, 0)`. When
`clicks = n`, `p_hat = 1` and the interval collapses to `(1, 1)`. This is a known weakness of the
Wald interval (it does not account for edge uncertainty the way a Wilson or Clopper-Pearson interval
would), but the formula is what is being tested here, not a correction for it.

### Large `n`

`n` up to `10^9` means `n * clicks` style intermediate products (if computed naively) can exceed
what a fixed-width 32-bit integer holds in some languages; keeping the arithmetic in floating point
throughout avoids that.

## Explanation

`click_rate_band` computes `p_hat = clicks / n` directly, then `se = sqrt(p_hat * (1 - p_hat) / n)`
from that same `p_hat` (so `clicks = 0` or `clicks = n` naturally produces `se = 0`, since one of the
two factors in the numerator is exactly `0`), and returns `(p_hat, p_hat - z*se, p_hat + z*se)` with
`z` fixed at `1.959964`. Because `se` is computed from `p_hat` rather than re-derived from `clicks`
and `n` separately, the two collapse cases fall out of the same formula with no branch.
