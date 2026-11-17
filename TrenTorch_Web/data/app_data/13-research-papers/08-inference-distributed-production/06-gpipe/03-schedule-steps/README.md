---
name: research-gpipe-schedule-steps
title: 'GPipe: Steps in a Pipeline Schedule'
tags: [research-papers, systems, parallelism, pipeline]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A GPipe forward pass takes M plus S minus one time steps: the first micro-batch needs S steps to reach the last stage, and the remaining micro-batches follow one per step.

### From theory to code

Implement `schedule_steps(stages, micro)`, the length of the forward schedule.

### Constraints

- Returns an integer.

### Hints

<details>
<summary>Hint 1</summary>

Add the micro-batch count to the stage count and subtract one.

</details>

## Theory

### The simple version

The schedule length and the bubble come from the same grid: the bubble is the extra steps beyond the M useful ones on each stage.

### The formula

$$T = M + S - 1$$

### How NumPy/PyTorch actually implements this

Pipeline schedule visualizers draw this grid with one row per stage and one column per step.

## Explanation

The diagram of this schedule is a staircase; each stage is busy for M of the T steps.
