---
name: production-ml-ab-testing-rollback
title: 'A/B Testing a Model Change, and Rolling Back When It Loses'
tags: [mlops, probability-and-statistics]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`05-shadow-deployment` compares a candidate model's would-be outputs against the live model's, but never measures its effect on real USER OUTCOMES (does it actually convert more? engage more?). A/B testing is the step that does: split real traffic between the existing model (control) and the new one (treatment), measure a real outcome metric for each group, and use an actual statistical test — not gut feeling — to decide whether an observed difference is real or just noise, and whether to roll back.

### From theory to code

Implement `assign_variant` (deterministic, weighted traffic splitting — generalizing `04-canary-deployment`'s single-percentage routing to several named variants), `evaluate_ab_test` (a genuine two-proportion z-test), and `decide_rollback`.

### Constraints

- `assign_variant(user_id, variant_names, weights)` deterministically assigns the SAME `user_id` to the SAME variant every time, with the population split roughly proportional to `weights`.
- `evaluate_ab_test(...)` computes the standard two-proportion z-test comparing control vs. treatment conversion rates, returning `(z_statistic, p_value)` — a POSITIVE `z_statistic` means control outperformed treatment.
- `decide_rollback(z_statistic, p_value, alpha=0.05)` returns `True` ONLY when the result is BOTH statistically significant (`p_value < alpha`) AND in the wrong direction (treatment underperforming, `z_statistic > 0`).
- Rolling back must never trigger just because a result is significant — the DIRECTION matters just as much as the significance.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`assign_variant` reuses `04-canary-deployment`'s hash-bucketing idea, just generalized: instead of one threshold (canary vs. not), walk through each variant's weight, accumulating a running total, and return the first variant whose cumulative weight exceeds the user's hashed position.

</details>

<details>
<summary>Hint 2</summary>

The standard normal CDF needed for the z-test's p-value can be computed with Python's own `math.erf` (`0.5 * (1 + erf(x / sqrt(2)))`) — no external statistics library required, and it's the exact same underlying math `scipy.stats.norm.cdf` would give you.

</details>

## Theory

### The simple version

Imagine two chefs each cooking for half of a restaurant's customers on the same night, and at the end of the night, comparing how many customers from each chef's half asked for seconds — if chef B's numbers are only SLIGHTLY lower, that could easily just be random luck in who happened to be seated on which side. A real statistical test asks the sharper question: "given how much natural night-to-night variation there normally is, is this big enough of a gap to conclude chef B's food is ACTUALLY worse, or is this within the range of coincidence?" A/B testing applies exactly this reasoning to a model change, using real visitor/conversion counts instead of chefs and customers.

### The formula

```text
assign_variant(user_id, names, weights):
    bucket = hash(user_id) mod 10000
    threshold = (bucket / 10000) * sum(weights)
    walk names/weights, accumulating weight, return first variant whose
    cumulative weight exceeds threshold

evaluate_ab_test (two-proportion z-test):
    p_control = conversions_control / visitors_control
    p_treatment = conversions_treatment / visitors_treatment
    p_pooled = (both conversions) / (both visitors)
    standard_error = sqrt(p_pooled * (1-p_pooled) * (1/visitors_control + 1/visitors_treatment))
    z = (p_control - p_treatment) / standard_error
    p_value = 2 * (1 - normal_cdf(|z|))

decide_rollback(z, p, alpha) = (p < alpha) AND (z > 0)
```

The direction check (`z > 0`) is doing real, non-trivial work here: without it, a SIGNIFICANTLY BETTER treatment (a genuine win!) would get flagged for rollback just as readily as a significantly worse one — a rollback rule that can't distinguish "significantly better" from "significantly worse" is worse than useless.

### How PyTorch actually implements this

Context only, untested by your submission: this exact two-proportion z-test is the standard statistical backbone behind real production A/B testing frameworks — the deterministic, hash-based variant assignment scheme (rather than re-randomizing per-request) is likewise standard practice, since it guarantees a returning user has a consistent experience for the full duration of the test, which is essential for measuring genuine behavioral effects rather than noise from inconsistent assignment.

## Explanation

`assign_variant` generalizes `04-canary-deployment`'s hash-based routing from a single canary threshold to an arbitrary list of weighted variants — `tests.py` confirms deterministic, sticky assignment for a given user, that the population split across many users roughly matches the requested weights, and that the function never returns anything outside the given variant names.

`evaluate_ab_test` implements the standard two-proportion z-test directly, using `math.erf` for the normal CDF rather than depending on `scipy` (which isn't part of this project's browser-based Python runtime) — `tests.py` confirms the sign and significance behave correctly across a clearly-worse, clearly-better, and statistically-indistinguishable treatment.

`decide_rollback` combines significance and direction into the actual go/no-go rule — `tests.py`'s final oracle test specifically confirms a SIGNIFICANTLY BETTER treatment is never rolled back, directly ruling out a mutant that checks only `abs(z) > 0` or otherwise ignores which direction the significant difference actually points.
