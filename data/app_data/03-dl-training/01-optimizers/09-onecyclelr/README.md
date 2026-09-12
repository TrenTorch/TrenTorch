---
name: dl-training-onecyclelr
title: OneCycleLR schedule, contrasted against warmup + cosine decay
tags: [optimizers, learning-rate, scheduling, training-dynamics]
difficulty: Advanced
---

## Statement

### The problem, from first principles

In `[08-lr-warmup-cosine-decay]` you built the schedule almost every large language model uses: ramp up, then decay down to (near) zero, spending most of training near the peak learning rate. Leslie Smith's "super-convergence" research asked a different question, aimed at a different regime: for models small enough to train in a handful of epochs, could you get away with a much more aggressive schedule, spending only a small fraction of training near the peak and instead using a MUCH larger peak learning rate than you'd normally dare use, tolerating some instability in the middle of the run in exchange for a shorter total training time? The answer was yes, and the resulting policy, "one-cycle," became the default in libraries like fastai for exactly this reason: it often reaches a target accuracy in fewer total epochs than a conventional schedule.

The mechanism is a single, symmetric-in-shape cycle across the whole run rather than a long flat plateau at the peak. Learning rate starts low, rises to a much higher-than-usual peak partway through training, then falls all the way down to a value far below where it started. The rising phase acts like an aggressive form of warmup (letting the model tolerate large steps once gradients have stabilized), and the falling phase acts like an aggressive annealing that settles the model into a sharp minimum by the very end.

### From theory to code

You'll implement `annealing_cos(start, end, pct)`, a helper that smoothly interpolates from `start` to `end` as `pct` sweeps from 0 to 1 along a cosine curve (this is the same shape as the second half of `[08-lr-warmup-cosine-decay]`'s `cosine_decay_lr`, but generalized to an arbitrary start and end value instead of assuming the start is always `base_lr`). Then `onecycle_lr(step, total_steps, max_lr, pct_start, div_factor, final_div_factor)` computes two derived boundary values, `initial_lr = max_lr / div_factor` and `min_lr = initial_lr / final_div_factor`, and a phase boundary `step_up = pct_start * total_steps`. For `step <= step_up`, use `annealing_cos` to interpolate from `initial_lr` up to `max_lr`. For `step > step_up`, use `annealing_cos` again to interpolate from `max_lr` down to `min_lr`, over the remaining `total_steps - step_up` steps.

### Constraints

- `annealing_cos(start, end, 0)` must return exactly `start`, and `annealing_cos(start, end, 1)` must return exactly `end`.
- `onecycle_lr` at `step == 0` must return `initial_lr` (`max_lr / div_factor`), at `step == step_up` must return exactly `max_lr`, and at `step == total_steps` must return `min_lr` (`initial_lr / final_div_factor`).
- `min_lr` ends up FAR below `initial_lr` in practice: with the PyTorch defaults `div_factor=25` and `final_div_factor=1e4`, `min_lr` is `max_lr / 250000`, four orders of magnitude smaller than where the schedule started.
- Assume `0 < pct_start < 1` and `total_steps > 0`.

### Hints

<details>
<summary>Hint 1: The interpolation formula</summary>

`annealing_cos(start, end, pct) = end + (start - end) / 2 * (1 + cos(pi * pct))`. Check the endpoints by hand: at `pct=0`, `cos(0)=1`, giving `end + (start-end) = start`. At `pct=1`, `cos(pi)=-1`, giving `end + 0 = end`.

</details>

<details>
<summary>Hint 2: Two phases, one helper</summary>

Both phases of `onecycle_lr` call the SAME `annealing_cos` helper, just with different `(start, end, pct)` arguments. Phase 1: `annealing_cos(initial_lr, max_lr, step / step_up)`. Phase 2: `annealing_cos(max_lr, min_lr, (step - step_up) / (total_steps - step_up))`, clamped to `pct <= 1` in case `step` overshoots `total_steps`.

</details>

<details>
<summary>Hint 3: Don't forget to re-derive initial_lr and min_lr</summary>

`div_factor` and `final_div_factor` are ratios, not learning rates themselves: `initial_lr = max_lr / div_factor` and `min_lr = initial_lr / final_div_factor`, computed once at the top of `onecycle_lr` before branching on which phase `step` falls into.

</details>

## Theory

### The simple version

Think of a sprinter's pacing strategy rather than a marathon runner's. A marathon runner (warmup + cosine decay) settles into a sustainable pace early and holds close to it for almost the whole race. A sprinter doing repeated intervals ramps up hard, pushes through a brief high-intensity peak, then deliberately decelerates to well below their starting pace to fully recover before the next rep. One-cycle training treats the entire run as a single such interval: a short rise, a brief peak at an unusually aggressive learning rate, and a long, deep cooldown.

### The formula

With `step_up = pct_start * total_steps`:

Rising phase (`step <= step_up`):

```
pct = step / step_up
lr(step) = max_lr + (initial_lr - max_lr) / 2 * (1 + cos(pi * pct))
```

Falling phase (`step > step_up`), with `step_down = total_steps - step_up`:

```
pct = (step - step_up) / step_down
lr(step) = min_lr + (max_lr - min_lr) / 2 * (1 + cos(pi * pct))
```

Both phases are the exact same cosine-interpolation shape, `annealing_cos`, just walked in opposite directions between different pairs of endpoints. This is why implementing `annealing_cos` once and calling it twice, rather than writing two separate formulas, mirrors how the underlying math actually works.

### How PyTorch actually implements this

`torch.optim.lr_scheduler.OneCycleLR` implements precisely this two-phase cosine anneal (its default `anneal_strategy='cos'`; it also supports a `'linear'` variant using straight-line interpolation instead of cosine). Its internal `_annealing_cos` helper is the same formula you derived above. One real implementation detail this question simplifies: PyTorch computes the phase-boundary step count with an internal integer offset (`int(pct_start * total_steps) - 1`) rather than the plain `pct_start * total_steps` used here, purely so the phase boundary lands on an exact integer step; the shape and endpoints of the schedule are identical either way. In practice, `OneCycleLR` is paired with `optimizer.step()` called once per batch (not once per epoch, since with few total epochs there often aren't enough per-epoch calls to trace out a meaningful cycle), and is frequently combined with `cycle_momentum=True`, which anneals the optimizer's momentum in the OPPOSITE direction of the learning rate: momentum is low while the learning rate is at its peak (to avoid overshooting) and high while the learning rate is low (to keep momentum-based methods like `[02-sgd-momentum]`'s `sgd_momentum_step` moving efficiently through flat regions).

## Explanation

`annealing_cos` implements `end + (start - end) / 2 * (1 + cos(pi * pct))` directly: this is a linear rescaling of the standard cosine wave (which itself ranges from `+1` down to `-1` as its argument sweeps from `0` to `pi`) onto the range `[start, end]`.

`onecycle_lr` first computes the two derived boundary learning rates, `initial_lr = max_lr / div_factor` and `min_lr = initial_lr / final_div_factor`, and the step at which the rising phase ends, `step_up = pct_start * total_steps`. It then branches: for `step <= step_up`, it computes `pct = step / step_up` and calls `annealing_cos(initial_lr, max_lr, pct)`, tracing the rising phase from `initial_lr` up to `max_lr`. For `step > step_up`, it computes `step_down = total_steps - step_up`, clamps `pct = min(1.0, (step - step_up) / step_down)` so calls past `total_steps` don't overshoot the cosine argument, and calls `annealing_cos(max_lr, min_lr, pct)`, tracing the falling phase from `max_lr` down to `min_lr`. Both phases reuse the same helper, only the `(start, end)` pair and the `pct` fraction change between them.
