---
name: systems-distributed-pipeline-parallelism-bubble-fraction
title: 'Note: Model/Pipeline Parallelism — Why Frontier Training Needs It, and What It Costs'
tags: [mlops, neural-networks, distributed-training]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`01-data-parallelism-gradient-averaging` assumes every worker can hold the WHOLE model — it just splits the batch. That assumption breaks for frontier-scale models that don't fit on a single GPU at all, which forces splitting the model itself instead: pipeline parallelism puts different LAYERS on different GPUs and streams "microbatches" through them like an assembly line — but an assembly line has a real, quantifiable cost: while it's filling up and draining, some stages are always sitting idle.

### From theory to code

Implement `pipeline_bubble_fraction(num_stages, num_microbatches)`, `pipeline_wall_time`, `ideal_wall_time`, and `pipeline_stage_utilization`, quantifying exactly how much of a pipeline's total runtime is wasted idle time ("bubble"), using the standard textbook pipeline-parallelism cost model.

### Constraints

- `pipeline_wall_time(p, m, t)` returns `(p - 1 + m) * t` — the `p - 1` steps needed to fill/drain the pipeline, plus `m` steady-state steps.
- `ideal_wall_time(m, t)` returns `m * t` — what a hypothetical zero-bubble pipeline would take.
- `pipeline_bubble_fraction(p, m)` returns `(p - 1) / (p - 1 + m)`, algebraically equal to `1 - ideal_wall_time / pipeline_wall_time`.
- `pipeline_stage_utilization(p, m)` returns `1.0 - pipeline_bubble_fraction(p, m)`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Think of `p - 1 + m` total time-steps: the first `p - 1` are spent filling the pipeline (only some stages have work yet) and draining it at the end, while the middle `m` steps have every stage genuinely busy. The bubble fraction is just (wasted steps) / (total steps).

</details>

<details>
<summary>Hint 2</summary>

`pipeline_bubble_fraction` doesn't need `pipeline_wall_time`/`ideal_wall_time` at all — it's the closed-form `(p - 1) / (p - 1 + m)` directly. The other two functions exist so `tests.py` can verify the closed form against the wall-time definition it came from.

</details>

## Theory

### The simple version

Imagine a factory assembly line with 4 stations, where each item takes exactly one time-step at each station. The very first item takes 4 time-steps to come off the line (it has to pass through all 4 stations), and the very last item's stations 1-3 sit idle waiting for it to arrive — but once the line is full, a new finished item comes off every single time-step. The "bubble" is exactly that fill-and-drain idle time at the start and end; the more items you run through the line, the smaller a fraction of the total time that fixed startup/drain cost becomes.

### The formula

```text
pipeline_wall_time(p, m, t) = (p - 1 + m) * t
ideal_wall_time(m, t)       = m * t

pipeline_bubble_fraction(p, m) = (p - 1) / (p - 1 + m)
                                = 1 - ideal_wall_time(m, t) / pipeline_wall_time(p, m, t)   [t cancels out]

pipeline_stage_utilization(p, m) = 1 - pipeline_bubble_fraction(p, m)
```

More pipeline stages `p` (needed for bigger models that don't fit on fewer GPUs) means more fill/drain overhead; more microbatches `m` per training step dilutes that fixed overhead across more useful work. This is exactly why pipeline-parallel training always tries to run with as many microbatches as memory allows — it's the only lever that shrinks the bubble without needing fewer pipeline stages.

### How PyTorch actually implements this

Context only, untested by your submission: this is the standard cost model from the GPipe paper (Huang et al., 2019), which introduced splitting a model's layers across devices and streaming microbatches through them exactly like this exercise's toy pipeline. Real frameworks (PyTorch's `torch.distributed.pipelining`, DeepSpeed's pipeline engine, Megatron-LM) use more sophisticated schedules (e.g. interleaved 1F1B) to shrink the bubble further, but they're all optimizing the exact same fill/drain tradeoff this formula quantifies.

## Explanation

`pipeline_wall_time` and `ideal_wall_time` encode the two reference points directly: the real pipeline's total time, and the time a magically bubble-free pipeline would take for the same amount of work.

`pipeline_bubble_fraction` is the closed-form ratio those two reference points reduce to — `tests.py` verifies this closed form is algebraically consistent with `1 - ideal_wall_time / pipeline_wall_time` for many `(p, m, t)` combinations, confirming the shortcut formula and the wall-time definition it's derived from agree.

`pipeline_stage_utilization` is simply the complement of the bubble fraction, framed the other way around — the fraction of time each stage spends doing genuinely useful work rather than waiting.
