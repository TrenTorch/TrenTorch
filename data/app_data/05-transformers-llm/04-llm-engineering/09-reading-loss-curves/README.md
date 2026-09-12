---
name: txf-llmeng-reading-loss-curves
title: 'Reading a loss curve: spotting training instability before it diverges'
tags: [transformers, nlp]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[04-seq-modeling/03-recurrent-neural-networks/03-bptt-vanishing-exploding]` demonstrated exploding gradients numerically, in isolation. In a REAL training run, the first visible symptom of exactly that kind of instability is usually a sudden, sharp SPIKE in the loss value, sometimes recovering on its own a few steps later, sometimes marking the start of a full, irrecoverable divergence (loss climbing toward infinity, or the model's weights becoming `NaN`). Catching an EARLY spike, before it turns into full divergence, is one of the most practically useful skills in actually training large models: catching it early might mean simply resuming from `[08-resume-from-checkpoint]`'s last good checkpoint with a lower learning rate, while catching it LATE can mean losing days of wasted compute to a run that silently diverged hours ago.

This question builds two concrete diagnostics directly from a raw loss history: a SPIKE detector (comparing each individual loss value against its own recent local baseline) and a DIVERGENCE detector (comparing a longer recent trend against the trend just before it), the same two questions a human staring at a live loss curve would actually be asking.

### From theory to code

Implement `detect_loss_spikes(loss_history, window, spike_ratio)` (flagging any step whose loss exceeds `spike_ratio` times the average of the preceding `window` steps) and `is_diverging(loss_history, window)` (comparing the average of the most recent `window` steps against the `window` steps before that).

### Constraints

- A spike at step `i` is compared against the average of steps `i - window` through `i - 1` (the LOCAL baseline immediately preceding it), never against the very start of training or the whole history.
- No spike can be flagged before at least `window` steps of history exist to compute a baseline from.
- `is_diverging` compares the MOST RECENT `window`-step average against the `window`-step average immediately BEFORE it, returning `False` (not an error) if fewer than `2 * window` total steps exist yet.

### Hints

<details>
<summary>Hint 1: Spike detection</summary>

```python
spikes = []
for i in range(window, len(loss_history)):
    baseline = sum(loss_history[i-window:i]) / window
    if loss_history[i] > spike_ratio * baseline:
        spikes.append(i)
return spikes
```

</details>

<details>
<summary>Hint 2: Divergence detection</summary>

```python
if len(loss_history) < 2 * window:
    return False
recent_mean = sum(loss_history[-window:]) / window
earlier_mean = sum(loss_history[-2*window:-window]) / window
return recent_mean > earlier_mean
```

</details>

## Theory

### The simple version

A doctor monitoring a patient's vital signs. A spike detector is like flagging any single reading that's WAY off from what that same patient's readings have looked like over the last few minutes, worth a closer look immediately, even if it turns out to be a brief, harmless fluctuation. A divergence detector is a longer-horizon check: comparing this HOUR's average reading against the PREVIOUS hour's average, looking for a genuine, sustained trend in the wrong direction, not just one noisy blip, the kind of pattern that actually warrants real intervention.

### The formula

```
spike at step i:  loss[i] > spike_ratio * mean(loss[i-window : i])

is_diverging:  mean(loss[-window:]) > mean(loss[-2*window : -window])
```

### How PyTorch actually implements this

There is no `torch.nn` loss-curve-monitoring utility (this is an OPERATIONAL, training-infrastructure concern, typically implemented in logging/monitoring code around a training loop, e.g. logged to Weights & Biases or TensorBoard and watched by automated alerting, not a model component). Real large-scale training runs (documented in the GPT-3, PaLM, and OPT technical reports, among others) routinely encounter loss spikes, and the standard mitigation is exactly what this question's diagnostics enable catching EARLY: `[08-resume-from-checkpoint]`'s checkpoint restore, often combined with skipping the specific batch that triggered the spike (in case it was simply a bad or corrupted training example) or temporarily lowering the learning rate before resuming.

## Explanation

`detect_loss_spikes` walks through `loss_history` starting from index `window` (the earliest point with a full `window`-step baseline available), computes the average of the PRECEDING `window` steps at every position, and flags that step if its own loss exceeds `spike_ratio` times that local baseline, a comparison against RECENT local behavior rather than the training run's entire history (which would make an early, expected high loss look identical to a genuinely alarming late-stage spike). `is_diverging` instead looks at TRENDS rather than individual points: it compares the average loss over the most recent `window` steps against the average over the `window` steps immediately before that, returning `True` only when the more recent window is genuinely WORSE on average, a sustained direction rather than a single noisy fluctuation, and returns `False` outright when there isn't yet enough history (fewer than `2 * window` steps) to make that comparison meaningfully at all.
