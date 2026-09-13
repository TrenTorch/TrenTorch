---
name: systems-perf-iterative-pruning-schedule
title: 'Stretch: Iterative Pruning Schedule'
tags: [mlops, neural-networks, compression]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`01-magnitude-pruning` zeros out a fixed fraction of weights in a single shot. Pruning a large fraction all at once tends to genuinely hurt accuracy — the network hasn't had any chance to adapt its remaining weights to compensate for what was just removed. Spreading the same total amount of pruning across many smaller steps, interleaved with retraining between them in a real pipeline, tends to reach the same final sparsity with far less accuracy loss.

### From theory to code

Implement `cubic_sparsity_schedule(step, total_steps, target_sparsity)`, which computes how much sparsity to reach _by_ a given step, and `iterative_prune(weight, target_sparsity, num_steps)`, which applies `01-magnitude-pruning`'s `magnitude_prune` repeatedly, once per step, following that schedule.

### Constraints

- `cubic_sparsity_schedule(0, ...)` returns `0.0`; `cubic_sparsity_schedule(total_steps, ...)` returns `target_sparsity` exactly.
- The schedule is monotonically increasing and front-loaded (covers most of the sparsity increase in the earlier steps, tapering off as it approaches the target).
- A `step` beyond `total_steps` clamps to `target_sparsity`.
- `iterative_prune` returns a list of `num_steps` arrays, each pruned to that step's scheduled sparsity, with sparsity never decreasing from one step to the next.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`progress = step / total_steps` goes from `0` to `1` — the cubic schedule is `target_sparsity * (1 - (1 - progress)**3)`, which starts at `0` and reaches `target_sparsity` exactly when `progress = 1`.

</details>

<details>
<summary>Hint 2</summary>

`iterative_prune` is a loop over `range(1, num_steps + 1)`, calling `magnitude_prune(weight, cubic_sparsity_schedule(step, num_steps, target_sparsity))` at each step — always pruning the _original_ `weight`, not the previous step's already-pruned result, since each step's sparsity target already accounts for everything pruned before it.

</details>

## Theory

### The simple version

Think of a cubic pruning schedule like editing a rough draft down to a final, polished piece: the biggest, easiest cuts happen early, when there's the most obviously-unnecessary material to remove — but as the draft gets tighter, each remaining cut has to be made more carefully, so the pace of cutting slows down even though the total amount removed keeps growing toward the same final target.

### The formula

```text
progress(step) = step / total_steps
cubic_sparsity_schedule(step) = target_sparsity * (1 - (1 - progress(step))^3)

iterative_prune(weight, target_sparsity, num_steps):
    for step in 1..num_steps:
        sparsity_this_step = cubic_sparsity_schedule(step, num_steps, target_sparsity)
        results.append(magnitude_prune(weight, sparsity_this_step))
    return results
```

### How PyTorch actually implements this

Context only, untested by your submission: this exact cubic schedule (with an initial sparsity of `0`, as used here) is the one published in Zhu & Gupta's "To prune, or not to prune" (2017) and used as the default pruning schedule in TensorFlow's Model Optimization Toolkit — verified directly in this exercise's own `tests.py`, whose `test_11_matches_the_published_cubic_pruning_schedule_formula` checks the schedule's output against that published formula's own algebra. PyTorch's `torch.nn.utils.prune` module supports pruning on a schedule via repeated calls interleaved with fine-tuning, exactly the workflow `iterative_prune` demonstrates in miniature (without the interleaved retraining a real pipeline would add between steps).

## Explanation

`cubic_sparsity_schedule` clamps `step >= total_steps` directly to `target_sparsity` (avoiding any floating-point rounding surprise at the exact final step), and otherwise computes `progress = step / total_steps` and applies the cubic formula — `(1 - progress)^3` shrinks quickly at first (large early progress) and slowly near the end (small late progress), which is exactly what makes the schedule front-loaded.

`iterative_prune` loops over `step` from `1` to `num_steps`, computing that step's target sparsity via `cubic_sparsity_schedule` and calling `magnitude_prune` on the _original_ `weight` each time (not on the previous step's result) — since each step's `sparsity` already represents the cumulative fraction that should be zeroed by that point, re-applying `magnitude_prune` from scratch at each step's own target sparsity produces the correct result without needing to track which specific elements were pruned at earlier steps.
