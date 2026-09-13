---
name: production-ml-model-degradation-retrain-trigger
title: 'Model Degradation Over Time, and Deciding When to Retrain'
tags: [mlops]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`02-concept-drift-sliding-window` detects that degradation has ALREADY happened, by looking back at recent performance. A production team also wants the forward-looking question answered: given how fast a model is currently degrading, how much longer does it have before it needs attention — and, right now, has it already crossed the line?

### From theory to code

Implement `has_model_degraded` (the actual current-state check), `predicted_future_metric` (a simple linear extrapolation), `days_until_degraded` (turning that extrapolation into an actionable countdown), and `should_retrain_now`.

### Constraints

- `has_model_degraded(current_metric, baseline_metric, tolerance)` returns `True` when the metric has dropped by MORE than `tolerance` below baseline (strict inequality).
- `predicted_future_metric(current_metric, degradation_rate_per_day, days_ahead)` returns `current_metric - degradation_rate_per_day * days_ahead`.
- `days_until_degraded(...)` returns `math.inf` for a zero-or-negative degradation rate, `0.0` if already past the threshold, and otherwise the remaining "budget" divided by the rate.
- `should_retrain_now` is built directly on top of `has_model_degraded`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The "degradation budget" is exactly how much the metric could still fall before crossing the degraded threshold: `current_metric - (baseline_metric - tolerance)` — divide that by the daily rate of loss to get how many days remain.

</details>

<details>
<summary>Hint 2</summary>

If the degradation budget is already `<= 0`, the model has ALREADY crossed the threshold right now — `days_until_degraded` should return `0.0` in that case, not a negative number.

</details>

## Theory

### The simple version

Imagine a car's fuel gauge that not only shows how much fuel is left RIGHT NOW, but also (given the current rate of consumption) estimates how many more miles you can drive before running out — one number answers "is there a problem right now," the other answers "how much runway do I have before there IS one." This exercise builds both versions of that question for a deployed model's performance metric instead of a car's fuel tank.

### The formula

```text
has_model_degraded(current, baseline, tolerance) = (baseline - current) > tolerance

predicted_future_metric(current, rate, days_ahead) = current - rate * days_ahead

days_until_degraded(current, baseline, tolerance, rate):
    if rate <= 0: return infinity                       -- never degrading
    budget = current - (baseline - tolerance)
    if budget <= 0: return 0.0                           -- already degraded
    return budget / rate

should_retrain_now(...) = has_model_degraded(...)
```

A faster degradation rate must ALWAYS predict FEWER remaining days, never more — this exercise's `tests.py` confirms this inverse relationship directly, since a formula that accidentally multiplied by the rate instead of dividing by it would (nonsensically) predict a faster-failing model has MORE runway left.

### How PyTorch actually implements this

Context only, untested by your submission: this reflects real, practical MLOps monitoring practice — teams track a model's key metric over time on a dashboard, often overlaying exactly this kind of simple linear trend line to get an early warning estimate of "at this rate, we'll need to retrain by roughly this date," well before the metric actually crosses whatever hard threshold `has_model_degraded` checks.

## Explanation

`has_model_degraded` is a direct threshold comparison — `tests.py` confirms the boundary is exclusive (a drop exactly equal to the tolerance does NOT count as degraded).

`predicted_future_metric` is a plain linear extrapolation, useful on its own as a "what if" projection.

`days_until_degraded` builds a genuinely more useful, actionable number out of that same extrapolation — `tests.py` confirms the two documented edge cases (a non-positive rate returning infinity, an already-crossed threshold returning zero) and, via its final oracle test, that the result scales correctly INVERSELY with the degradation rate, directly ruling out a mutant that multiplies instead of divides.

`should_retrain_now` is deliberately kept as its own thin wrapper around `has_model_degraded` — a real system's retraining DECISION logic staying decoupled from the underlying degradation DEFINITION, even though today the two happen to be identical, is exactly the kind of separation that makes it easy to later swap in a more sophisticated retraining policy without touching the degradation check itself.
