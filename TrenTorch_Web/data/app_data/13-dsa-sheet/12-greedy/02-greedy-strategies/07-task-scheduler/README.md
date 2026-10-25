---
name: sheet-task-scheduler
title: 'Task Scheduler'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Advanced
---

## Statement

`tasks` is a string where each letter is a task of one time unit. You may run the tasks in **any order**, and in each time unit you do one task or stay **idle**. The **same letter** needs at least `n` other time units (tasks or idle) between two runs. Return the **least number of time units** to finish all tasks.

For `tasks = "AAABBB"` and `n = 2` the answer is `8` (`A B _ A B _ A B`).

### Examples

**Example 1**

Input:

```python
least_interval('AAABBB', 2)
```

Output:

```text
8
```

**Explanation:** The schedule A B _ A B _ A B uses two idle slots to keep the same letters at least 2 apart, giving 8 total time units.

**Example 2**

Input:

```python
least_interval('AAABBB', 0)
```

Output:

```text
6
```

**Explanation:** With n = 0 no idle gap is required, so the six tasks run consecutively, taking exactly six time units.

### Constraints

- `0 <= len(tasks) <= 200000`
- `0 <= n <= 100`
- Upper-case letters.

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

The most frequent task decides the schedule. Say task `A` appears `m` times. Lay it out first: `A` followed by `n` slots, repeated, with the last `A` at the end. That frame has `(m - 1) * (n + 1) + 1` positions. All the other tasks fill the empty slots, and any tasks that do not fit simply make the frame longer.

If several tasks appear `m` times (a tie for the maximum), each of them adds one more position at the end: let `ties` be their count. The answer is `max(len(tasks), (m - 1) * (n + 1) + ties)`: either the frame (with idle time) or, when there are enough tasks to leave no idle time, just the number of tasks.

A different view uses a **max-heap**: always run the available task with the most copies left. The formula is the same result without a simulation.

## Explanation

`m` is the largest count and `ties` the number of letters with that count. The frame length is the minimum when idle time is needed; with many different tasks the answer is just `len(tasks)`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                    | Variables                    |
| ---------------------------------- | ---------------------------- |
| `counts = {}`                      | `counts = {}`                |
| `counts[t] = counts.get(t, 0) + 1` | `counts = {'A': 1}, t = 'A'` |
| `counts[t] = counts.get(t, 0) + 1` | `counts = {'A': 2}`          |
| `for t in tasks:`                  | `counts = {'A': 3}, t = 'B'` |
| `counts[t] = counts.get(t, 0) + 1` | `counts = {'A': 3, 'B': 1}`  |
| `counts[t] = counts.get(t, 0) + 1` | `counts = {'A': 3, 'B': 3}`  |
| `m = max(counts.values())`         | `m = 3`                      |
| `return`                           | `returned = 8`               |
