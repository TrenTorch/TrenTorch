---
name: eval-nemenyi-cd
title: 'Nemenyi critical difference after the Friedman test'
tags: [classical-ml, evaluation, statistics, nemenyi, post-hoc]
difficulty: Advanced
---

## Statement

### Decide which pairs of models differ after a significant Friedman test

When the Friedman test rejects, the Nemenyi post-hoc test (Demsar, 2006) says which pairs differ. Two algorithms differ when their average ranks differ by at least the critical difference

`CD = q_alpha * sqrt(k (k + 1) / (6 N))`,

where `k` is the number of algorithms, `N` the number of datasets, and `q_alpha` is the studentized range statistic divided by `sqrt(2)` for the chosen `alpha`. For example, `q_0.05 = 2.569` when `k = 4`.

Implement two functions:

- `nemenyi_cd(k, n, q_alpha)` returns `CD` as a float.
- `significantly_different(rank_a, rank_b, cd)` returns `True` when `abs(rank_a - rank_b) >= cd`.

### Constraints

- `k >= 2`, `n >= 1`, and `q_alpha > 0`. Otherwise raise `ValueError` from `nemenyi_cd`.
- `cd` must be nonnegative. Otherwise raise `ValueError` from `significantly_different`.
- The comparison is inclusive: a gap exactly equal to `cd` counts as significant.

### Hints

<details>
<summary>Hint 1</summary>

The critical difference grows with the square root of `k (k + 1)` and shrinks with the square root of `N`.

</details>

## Theory

The Nemenyi test is conservative: it controls the familywise error across all pairs by using the studentized range distribution. The consequence is that with few datasets, the critical difference can be wide enough to hide real differences. Demsar's critical-difference diagram is the usual way to show the result, with models joined by a bar when they are not significantly different. Reporting the diagram is more useful than a list of p-values, because it shows the ranking and the uncertainty at once.

### Where this shows up in production

Model-selection write-ups for families of candidate models, such as a set of gradient boosters, linear models, and small neural nets tested across many tasks, use critical-difference diagrams to name the group of models that are statistically tied. That group is the shortlist for further tuning.

### Using it to make decisions

Run this only after a significant Friedman test, and only with enough datasets that the critical difference is smaller than the rank gaps you care about. If the CD is wider than the whole range of average ranks, adding datasets will probably give a better answer than more models or more tuning. Report which models are tied, then choose among them on cost, latency, or maintenance.

### Pros and cons

**Pros:** simple closed form, works with any number of models, and produces an easy-to-read diagram.

**Cons:** very conservative, so it can miss real differences, it depends on tabulated `q_alpha` values, and it cannot say how large a difference is, only whether it passes the threshold.

## Explanation

The solution multiplies `q_alpha` by the square-root factor that depends only on `k` and `N`. The significance check is a single absolute-difference comparison, which keeps the decision rule identical to the diagram a reader will draw.
