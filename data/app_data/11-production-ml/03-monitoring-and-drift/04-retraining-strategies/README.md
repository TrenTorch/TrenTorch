---
name: production-ml-retraining-strategies
title: 'Retraining Strategies: Scheduled, Triggered, and Online Learning'
tags: [mlops]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`03-model-degradation-retrain-trigger` built the DECISION of whether a model needs retraining — but "when do we actually retrain?" has at least three genuinely different real answers, each with a different cost/responsiveness tradeoff: retrain on a fixed calendar schedule regardless of need, retrain only when degradation is actually detected, or never really "retrain" as a discrete event at all, instead nudging the model continuously with every new labeled example.

### From theory to code

Implement `scheduled_retrain_due`, `triggered_retrain_due` (built directly on `03-model-degradation-retrain-trigger`'s `has_model_degraded`), and `online_update_step`, a genuine single-example gradient descent update.

### Constraints

- `scheduled_retrain_due(days_since_last_retrain, schedule_interval_days)` returns `True` once the interval has elapsed, regardless of any performance signal.
- `triggered_retrain_due(current_metric, baseline_metric, tolerance)` returns exactly `has_model_degraded`'s result.
- `online_update_step(weight, bias, x, y, learning_rate)` performs one step of gradient descent on the squared error `(weight*x + bias - y)^2`, returning the updated `(weight, bias)`.
- The online update must always move `(weight, bias)` in a direction that DECREASES that squared error (for a small enough learning rate).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Scheduled and triggered retraining answer genuinely INDEPENDENT questions — a model can be well within tolerance (triggered says "no need") while still being well past its scheduled interval (scheduled says "yes, due anyway"), or vice versa.

</details>

<details>
<summary>Hint 2</summary>

`online_update_step`'s gradient is exactly the same chain-rule computation `linear-regression-mse-gradient`'s Theory built up, specialized to a single scalar `x`/`y` pair instead of a whole batch: `grad_weight = 2 * x * error`, `grad_bias = 2 * error`, where `error = (weight*x + bias) - y`.

</details>

## Theory

### The simple version

Imagine three different approaches to car maintenance: getting an oil change every 5,000 miles regardless of the car's actual condition (scheduled — simple, predictable, sometimes wasteful, sometimes too late), getting one only when a dashboard warning light actually comes on (triggered — responsive, but requires the warning system to be reliable and continuously monitored), or a hypothetical car that continuously, imperceptibly replenishes its own oil a tiny bit with every mile driven, so there's never really a discrete "maintenance event" at all (online learning). All three are legitimate strategies; which one makes sense depends entirely on how expensive "maintenance" is, how fast things actually degrade, and how much monitoring infrastructure is available.

### The formula

```text
scheduled_retrain_due(days_since, interval) = days_since >= interval

triggered_retrain_due(current, baseline, tolerance) = has_model_degraded(current, baseline, tolerance)

online_update_step (one step of SGD on a single example):
    prediction = weight * x + bias
    error = prediction - y
    grad_weight = 2 * x * error
    grad_bias = 2 * error
    new_weight = weight - learning_rate * grad_weight
    new_bias = bias - learning_rate * grad_bias
```

Online learning is the most responsive of the three (the model adapts continuously, with no "stale" period at all), but it's also the riskiest: a single unusual or mislabeled example nudges the model immediately, with no batch-level averaging to smooth out noise — a real, genuine tradeoff, not a strictly-better replacement for the other two strategies.

### How PyTorch actually implements this

Context only, untested by your submission: all three strategies are standard, real practices in production ML — scheduled retraining (a nightly or weekly pipeline run) is the simplest to operate; triggered retraining (based on exactly the kind of drift/degradation signals `01`-`03` in this track compute) is more efficient but requires reliable monitoring; and online learning (used in systems like ad-click prediction, where feedback arrives continuously and in huge volume) trades batch-level stability for maximal responsiveness to a constantly-shifting environment.

## Explanation

`scheduled_retrain_due` is a plain threshold comparison against elapsed time, with zero awareness of actual model performance — deliberately simple.

`triggered_retrain_due` delegates directly to `03-model-degradation-retrain-trigger`'s already-verified `has_model_degraded` — `tests.py` confirms scheduled and triggered decisions are genuinely INDEPENDENT signals (a model can be due by one criterion and not the other).

`online_update_step` implements one real gradient-descent step on a single example's squared error — `tests.py` verifies the step genuinely decreases the loss, matches a hand-computed example exactly, converges toward a perfect fit over many repeated updates on the same example, and — via its final oracle test — matches a true finite-difference numerical gradient estimate, directly ruling out a mutant that drops the factor of `2` when differentiating the squared error term (an easy, common calculus slip that finite-difference checking catches reliably).
