---
name: dl-training-lr-warmup-cosine-decay
title: Learning rate scheduling: warmup and cosine decay
tags: [optimizers, learning-rate, scheduling, training-dynamics]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Picture training a large transformer from a freshly initialized set of weights. At step 0, every weight is essentially random noise, and the gradients you compute from the first few batches are enormous and unreliable: the model hasn't seen enough data yet to know which direction is actually "downhill." If you slam in the full learning rate immediately, Adam's second-moment estimate `v` is still close to zero (it hasn't accumulated enough history), so the bias-corrected update `m_hat / (sqrt(v_hat) + eps)` can spike to a huge value on the very first few steps. That spike can permanently damage the weights: a large early update can push a layer into a bad region it never recovers from, or blow up activations to `inf`/`nan` before training has barely started. This is a well documented, reproducible failure mode, not a theoretical concern.

The fix that essentially every modern large-model training run uses is to not start at the target learning rate at all. Instead, ramp the learning rate up from (near) zero over the first few hundred or thousand steps ("warmup"), giving Adam's moment estimates time to stabilize before the model takes full-sized steps. Then, once training is underway, the learning rate can't just stay at its peak forever either: late in training, you want small, careful updates that fine-tune the model into a good minimum rather than continuing to bounce around with large steps. So after warmup, the learning rate decays, typically following a smooth cosine curve down toward a small final value (often zero) by the end of training.

### From theory to code

You'll implement the three pieces separately, then compose them. First, `linear_warmup_lr(step, warmup_steps, base_lr)`: a straight linear ramp from 0 up to `base_lr`, reaching `base_lr` exactly when `step == warmup_steps` and holding there if called for a larger step. Second, `cosine_decay_lr(step, total_steps, base_lr, min_lr)`: takes a fraction ("progress") through `[0, total_steps]` and maps it through one half-period of a cosine curve from `base_lr` down to `min_lr`, landing exactly on `min_lr` at `step == total_steps` and holding there afterward. Third, `warmup_cosine_lr(step, warmup_steps, total_steps, base_lr, min_lr)`: the schedule an actual training loop calls once per step. It should reuse the two functions above rather than reimplementing their formulas: for `step < warmup_steps`, delegate to `linear_warmup_lr`; for `step >= warmup_steps`, delegate to `cosine_decay_lr`, but re-based so the decay phase's own internal step counter starts at 0 the moment warmup ends (i.e. pass `step - warmup_steps` as the decay step, and `total_steps - warmup_steps` as the decay phase's own length).

### Constraints

- `linear_warmup_lr` must return exactly `0.0` at `step == 0` and exactly `base_lr` at `step == warmup_steps` (and stay at `base_lr` for any `step > warmup_steps`, since the function may be called past its own valid warmup range by a caller that forgot to branch, guard against that).
- `cosine_decay_lr` must return exactly `base_lr` at `step == 0` and exactly `min_lr` at `step == total_steps`, holding at `min_lr` afterward.
- `warmup_cosine_lr` must be continuous at the `step == warmup_steps` boundary: the value returned for `step == warmup_steps` should equal `base_lr`, matching both what warmup ends at and what decay starts at.
- Assume `warmup_steps < total_steps` and all inputs are non-negative.

### Hints

<details>
<summary>Hint 1: Where do you start?</summary>

Write `linear_warmup_lr` first in isolation: it's `base_lr * min(1, step / warmup_steps)`. The `min(1, ...)` is what makes it hold flat at `base_lr` once `step` passes `warmup_steps`, instead of continuing to climb past it.

</details>

<details>
<summary>Hint 2: The cosine formula</summary>

A raw cosine goes from `+1` down to `-1` as its argument goes from `0` to `pi`. Rescale: `progress = min(1, step / total_steps)`, then `lr = min_lr + 0.5 * (base_lr - min_lr) * (1 + cos(pi * progress))`. Check the two ends by hand: at `progress = 0`, `cos(0) = 1`, giving `min_lr + (base_lr - min_lr) = base_lr`. At `progress = 1`, `cos(pi) = -1`, giving `min_lr + 0 = min_lr`.

</details>

<details>
<summary>Hint 3: Composing the two phases</summary>

`warmup_cosine_lr` should not duplicate either formula. Branch on `step < warmup_steps`, and in the decay branch, remember the decay function needs to see its OWN step count starting from 0, not the global step count: pass `step - warmup_steps` for its `step` argument and `total_steps - warmup_steps` for its `total_steps` argument.

</details>

## Theory

### The simple version

Think of merging onto a highway. You don't floor the accelerator the instant you leave the on-ramp: you'd lose control before your tires have even found their grip on the road. You accelerate smoothly up to highway speed (warmup), cruise near peak speed for a while, then start braking well before your exit so you come to a controlled stop rather than slamming on the brakes at the last second (cosine decay). The "grip" analogy maps directly onto Adam: the optimizer's momentum and variance estimates (`m` and `v`) need a few steps of real gradient data before they're trustworthy, so the learning rate should be small while they're still warming up.

### The formula

Warmup phase (`step <= warmup_steps`):

```
lr(step) = base_lr * (step / warmup_steps)
```

Decay phase (`step > warmup_steps`), with `T = total_steps - warmup_steps` and `s = step - warmup_steps`:

```
progress = s / T
lr(step) = min_lr + 0.5 * (base_lr - min_lr) * (1 + cos(pi * progress))
```

This is exactly one half of a cosine wave: at `progress = 0` it sits at the peak (`base_lr`), and it descends smoothly, with zero slope at both ends, down to `min_lr` at `progress = 1`. The "zero slope at both ends" property is why cosine decay is preferred over a straight linear decay in practice: there's no sudden kink in the learning rate curve at the point where warmup ends and decay begins, or at the very end of training.

### How PyTorch actually implements this

PyTorch does not ship a single built-in class that does "linear warmup then cosine decay" out of the box; `torch.optim.lr_scheduler.CosineAnnealingLR` does cosine decay only, with no warmup phase. The most common real-world pattern is a `SequentialLR` that chains `LinearLR` (for warmup) into `CosineAnnealingLR` (for decay), switching over at a `milestones=[warmup_steps]` boundary, exactly the two-phase branch you implemented in `warmup_cosine_lr`. Hugging Face's `transformers` library, used to train the overwhelming majority of published language models, ships this exact schedule under the name `get_cosine_schedule_with_warmup`, and its source computes precisely the formula above. Under the hood, every PyTorch LR scheduler works by computing a multiplicative factor against the optimizer's `base_lr` and writing it into `optimizer.param_groups[i]['lr']` once per call to `scheduler.step()`, which is why schedulers are always called once per optimizer step, in between `optimizer.step()` and the next `loss.backward()`. You've already built the piece this all rests on: `[08-adamw-decoupled-weight-decay]`'s `adam_step`/`adamw_step` take `lr` as a plain float argument, which is exactly the value a scheduler like this one recomputes and re-injects at every step of training.

## Explanation

`linear_warmup_lr` computes `base_lr * min(1.0, step / warmup_steps)`: the `min` clamps the ratio at 1 once `step` reaches or passes `warmup_steps`, so the function can never overshoot `base_lr`.

`cosine_decay_lr` computes `progress = min(1.0, step / total_steps)`, then plugs it into `min_lr + 0.5 * (base_lr - min_lr) * (1 + cos(pi * progress))`: this is the half-cosine curve derived above, and the `min` clamp again prevents the curve from being evaluated past `progress = 1` (where cosine would start rising back up).

`warmup_cosine_lr` is a pure dispatcher: it checks `step < warmup_steps` and calls `linear_warmup_lr` unchanged for the warmup phase; otherwise it computes `decay_step = step - warmup_steps` and `decay_total_steps = total_steps - warmup_steps`, re-basing the step counter to start at 0 for the decay phase, and calls `cosine_decay_lr` with those re-based values. Because both branches agree exactly at `step == warmup_steps` (warmup returns `base_lr`, and decay at `decay_step == 0` also returns `base_lr`), the composed schedule has no discontinuity at the seam.
