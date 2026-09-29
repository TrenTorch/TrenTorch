---
name: agentic-loop-stop-step-time-budget
title: Stop an Agent Loop With a Step and Time Budget
tags: [agentic-systems, agent-loop, orchestration]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A ReAct loop needs more than one way to stop. The model finishing on its own is the happy path, but nothing guarantees it ever will — a confused model can loop forever, chasing the same dead end. Two independent safety nets exist for exactly this: a hard cap on the number of steps, and a hard cap on wall-clock time, since a handful of very slow tool calls could blow the time budget long before the step count does. A real loop has to check all three conditions, every step, in a well-defined order.

### From theory to code

You're given the full log of steps a run actually took: `(elapsed_seconds_after_this_step, action)`, in order, where `elapsed_seconds` is cumulative from the run's start. Implement `find_loop_stop(steps, max_steps, max_seconds)`. Walk the steps in order (1-indexed), and at each step check, **in this priority order**, the first condition that applies:

1. `action == "finish"` -> `(step_number, "FINISHED")`
2. `step_number >= max_steps` -> `(step_number, "STEP_BUDGET")`
3. `elapsed_seconds >= max_seconds` -> `(step_number, "TIME_BUDGET")`

Return `(stop_step, reason)` for whichever condition trips first.

### Constraints

- 1 to 50 steps in the log; `max_steps >= 1`, `max_seconds > 0`.
- The log is guaranteed to trip at least one of the three conditions by its last entry.

### Hints

<details>
<summary>Hint 1</summary>

Check the three conditions in the exact order given, as three separate `if` statements each returning immediately — not as a single combined boolean expression. When more than one condition is true at the same step, the priority order (not evaluation order of an `or` chain) is what decides which reason gets reported.

</details>

<details>
<summary>Hint 2</summary>

`"finish"` always wins, even on a step that would _also_ have tripped the step or time budget. Check it first, unconditionally, before touching either budget.

</details>

## Theory

### The simple version

Three independent tripwires, checked in a fixed pecking order at every single step: did the model decide it's done, did we run out of allowed steps, did we run out of allowed time. The first one to fire, in that priority order, is the one that gets reported — even if a later-checked condition would also have fired on that same step.

### Why a fixed priority order, not "whichever condition is literally true first in real time"

At any given step, more than one condition might genuinely be true simultaneously (finishing exactly on the step-budget boundary, say). Without a defined priority, the reported reason would depend on implementation detail rather than being a deterministic, well-specified answer — and a monitoring system reading these reasons needs "FINISHED" to always mean the model actually decided to stop, never a budget coincidentally expiring on the same step.

### How this shows up in real systems

Every production agent loop needs both a step ceiling and a time ceiling, because they catch different failure modes: a step ceiling catches an agent that's technically fast but stuck in a long chain of small actions, while a time ceiling catches an agent that's making very few, very slow tool calls (a hanging API, a huge document to process) that would never trip a step count at all.

## Explanation

The function walks `steps` with `enumerate(..., start=1)` so the 1-indexed step number used in both the return value and the comparisons is the loop variable itself, not something computed separately. At each step, the three checks run as separate `if` statements in the exact priority order specified, each one returning immediately on a match — this is what guarantees `"FINISHED"` is reported whenever it applies, regardless of whether a budget condition would also have matched that same step, since the finish check runs and returns before either budget check is ever evaluated.
