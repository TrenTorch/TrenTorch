---
name: research-sgdr-cycles-total
title: 'SGDR: Total Steps Across Cycles'
tags: [research-papers, optimization, learning-rate-schedule, restarts]
difficulty: Beginner
---

## Statement

### The problem, from first principles

In SGDR the total training length is the sum of the cycle lengths. Knowing it lets you budget epochs for a given number of restarts.

### From theory to code

Implement `cycles_total(T0, Tmult, n)`, the total steps across the first n cycles.

### Constraints

- Count the first cycle as n = 1.

### Hints

<details>
<summary>Hint 1</summary>

Add each cycle length to a running total, multiplying the length by Tmult after each.

</details>

## Theory

### The simple version

The geometric growth means a few restarts already cover a long run, so the schedule suits budgets in epochs.

### The formula

$$\sum_{i=0}^{n-1}T_0\,T_{\text{mult}}^{\,i} = T_0\frac{T_{\text{mult}}^{n}-1}{T_{\text{mult}}-1}$$

### How NumPy/PyTorch actually implements this

Training planners compute this total to pick how many restarts fit a fixed budget.

## Explanation

Hand case: 10 + 20 + 40 = 70.
