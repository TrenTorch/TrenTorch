---
name: dl-training-metric-tracking
title: Basic metric tracking (loss curve)
tags: [neural-networks, training]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`[02-assemble-training-loop]`'s `train_one_epoch` returns a single average loss for that epoch, and you'd normally call it once per epoch, in a loop, for many epochs. Without recording every value it returns somewhere, you can only ever see the MOST RECENT epoch's loss, and lose the entire training history the moment training moves on to the next epoch, exactly the history you'd need to plot a loss curve, notice whether the model has started overfitting (`[04-regularization/01-early-stopping]`'s exact concern), or decide which checkpoint was actually the best one to keep.

Raw per-step or per-epoch loss values are also often genuinely noisy, jumping up and down step to step even while the overall trend is clearly decreasing, which is why loss curves in practice are almost always shown SMOOTHED (a moving average), rather than as the raw, jittery values.

### From theory to code

Implement `MetricTracker`, with `record(name, value)` (append a value to that metric's history), `get_history(name)` (return the raw list), `moving_average(name, window)` (return a same-length list of smoothed values, using a "trailing window" of up to `window` most recent values at each point), and `best(name, mode)` (return the minimum or maximum ever recorded for that metric, `mode="min"` or `mode="max"`).

### Constraints

- `moving_average` must return a list the SAME LENGTH as the raw history, one smoothed value per raw value, not a shorter list that skips the first few entries.
- For index `i` where fewer than `window` values exist so far (i.e. `i < window - 1`), average over whatever IS available (`values[0:i+1]`), don't wait until a full window has accumulated.
- `best(name, mode="min")` returns the minimum ever recorded; `mode="max"` returns the maximum. Return `None` (not an error, not `0`) if `name` was never recorded.
- Different metric names must be tracked completely independently.

### Hints

<details>
<summary>Hint 1: record and get_history</summary>

`self.history.setdefault(name, []).append(value)`: `setdefault` returns the existing list for `name` if one exists, or creates and returns a fresh empty list if this is the first time, either way you then `.append(value)` to it. `get_history` is just `self.history.get(name, [])`.

</details>

<details>
<summary>Hint 2: moving_average's trailing window</summary>

For each index `i` in `range(len(values))`, the window START is `max(0, i - window + 1)` (clamped at `0` so early entries use a partial window), and the window is `values[start : i+1]`. Average that slice and append it to the result list.

</details>

<details>
<summary>Hint 3: best</summary>

`min(values) if mode == "min" else max(values)`, but check `if not values: return None` FIRST, before calling `min`/`max` on a possibly-empty list (which would raise an error instead).

</details>

## Theory

### The simple version

A car's instant fuel-economy readout jumps around wildly, moment to moment, going uphill vs. downhill, accelerating vs. coasting, while the trip-average readout stays smooth and actually tells you something useful about your overall driving. Training loss is exactly the "instant" readout: individual steps or even individual epochs can be noisier than the underlying trend, because of which specific batch happened to get sampled, how the mini-batch's particular examples happened to be distributed. A moving average is the "trip average" view: it doesn't change what actually happened, but it makes the trend the raw numbers are hiding much easier to actually see.

### The formula

For a trailing moving average with window size `w`, at index `i` (0-indexed):

```
moving_average[i] = mean(values[max(0, i - w + 1) : i + 1])
```

At `i = 0`, this is just `values[0]` (a "window" of one value); once `i >= w - 1`, every subsequent entry averages exactly `w` values.

### How PyTorch actually implements this

There's no single built-in "MetricTracker" in PyTorch itself (PyTorch's job is computing tensors and gradients, not bookkeeping), but this exact pattern, recording a scalar once per step and later smoothing or aggregating it, is precisely what TensorBoard's `SummaryWriter.add_scalar(tag, value, step)` and Weights & Biases' `wandb.log({"loss": value})` do under the hood, and TensorBoard's own UI has a literal "smoothing" slider that applies almost exactly this kind of trailing (technically, in TensorBoard's specific case, exponentially-weighted rather than a flat trailing window) moving average to noisy training curves before plotting them. The `best()` method's real-world payoff is checkpoint selection: a training script typically calls `tracker.record("val_loss", val_loss)` once per epoch, and saves a new "best model" checkpoint file only when the CURRENT epoch's `val_loss` equals (or improves on) `tracker.best("val_loss")`, exactly the logic `[04-regularization/01-early-stopping]` builds on directly.

## Explanation

`record` uses `self.history.setdefault(name, []).append(value)`: `setdefault` handles both "first time this name is recorded" (creates an empty list) and "name already has history" (returns the existing list) in one call, and `get_history` mirrors it with `self.history.get(name, [])` for reads.

`moving_average` loops over every index `i` of the recorded values, computes `start = max(0, i - window + 1)` (the trailing window's start, clamped so it never goes negative), slices `values[start : i+1]`, and appends that slice's mean to the result. Because `start` is clamped at `0`, early indices (where fewer than `window` values exist yet) automatically average over whatever's actually available, without any special-casing.

`best` returns `None` immediately if `name`'s history is empty, otherwise returns `min(values)` or `max(values)` depending on `mode`, directly matching whichever comparison direction "better" means for that particular metric (lower loss is better; higher accuracy is better).
