---
name: inf-batch-latency-percentiles
title: 'Calculate P50, P95, and P99 Inference Latency'
tags: [inference, latency, percentiles, serving-metrics]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Averages hide tail behavior: a service with a 50ms average latency can still have some users waiting 2 seconds. Given a list of per-request latency measurements, compute the P50 (median), P95, and P99 latency percentiles using linear interpolation between the two nearest ranks — the standard method reported by serving dashboards.

### From theory to code

```
rank = p/100 * (n - 1)
percentile = sorted[floor(rank)] + (rank - floor(rank)) * (sorted[ceil(rank)] - sorted[floor(rank)])
```

### Constraints

- Use the `(n-1)`-based linear interpolation rank formula, not the `(n+1)`-based or nearest-rank method.
- Handle `n == 1` (all percentiles equal the single sample).
- Accept an arbitrary list of percentiles to compute (not hardcoded to just 50/95/99).

### Hints

<details>
<summary>Hint: Sort once, index repeatedly</summary>

Sort the array once, then just index it with `int(rank)` and `int(rank)+1` (clip the upper index to the last valid index) for each requested percentile — no need to re-sort per percentile.

</details>

## Theory

### The simple version

Percentiles answer "what latency does the worst X% of traffic experience?" — P50 is the typical experience, while P95 and P99 characterize the tail that matters most for user-perceived reliability and SLA compliance.

### The formula

```
rank = p/100 * (n - 1)
percentile = sorted[floor(rank)] + frac(rank) * (sorted[ceil(rank)] - sorted[floor(rank)])
```

Linear interpolation between ranks (rather than simply picking the nearest sample) is the standard definition used by most metrics libraries: it makes percentile estimates change smoothly as more samples are added, instead of jumping discretely.

### How PyTorch actually implements this

This is a pure numeric/statistics computation with no tensor operations to speak of; `numpy.percentile(arr, p, method='linear')` implements the exact same interpolation rule and can be used as a drop-in check.

## Explanation

The `(n-1)`-based rank formula places the 0th percentile exactly on the smallest sample and the 100th percentile exactly on the largest, with every other percentile linearly interpolated between the two neighboring sorted samples — which is what makes the estimate change smoothly rather than jump as new samples arrive. This smoothness matters in practice: a dashboard tracking P99 latency over time would show artificial step-jumps every time the sample count crossed a rank boundary under a nearest-rank method, which is exactly the noise linear interpolation avoids.
