---
name: agentic-loop-decompose-goal-subtasks
title: Decompose a Goal Into an Ordered Sub-Task List
tags: [agentic-systems, agent-loop, planning]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Deciding *what* the sub-tasks of a goal are is a creative, model-driven step — genuinely hard to test deterministically, since there's rarely one "correct" decomposition. But once the sub-tasks and their dependencies are known ("research the topic" has to happen before "write the draft," which has to happen before "proofread"), deciding what *order* to actually run them in is a completely mechanical problem: find any order that never runs a sub-task before something it depends on.

### From theory to code

You're given every sub-task's name and a list of `(before, after)` dependency pairs — `before` must be scheduled strictly earlier than `after`. The dependency graph is guaranteed acyclic (no sub-task can depend on itself, directly or transitively). Implement `order_subtasks(subtasks, dependencies)`. Produce a valid execution order respecting every dependency. When more than one sub-task is available to schedule next (no unscheduled dependency blocking it), prefer whichever one comes **first in the original `subtasks` list** — this is what makes the answer unique instead of "any valid order."

Return the full ordered list of sub-task names.

### Constraints

- 1 to 100 sub-tasks, distinct names.
- 0 to 500 dependency pairs; the dependency graph never contains a cycle.

### Hints

<details>
<summary>Hint 1</summary>

This is the standard "topological sort" problem, but the tie-break rule (prefer whatever's earliest in the original list) means you can't just use any topological sort algorithm off the shelf unmodified — a priority-queue-based approach keyed on "earliest in the original list among currently-schedulable tasks" is the direct way to get this specific tie-break, though a simple repeated linear scan over the original list works fine too at these bounds.

</details>

<details>
<summary>Hint 2</summary>

Track each sub-task's remaining "blockers" count (how many not-yet-scheduled dependencies it has). A sub-task becomes eligible to schedule the moment that count hits zero — recompute it incrementally as you schedule things, rather than rescanning the full dependency list on every step.

</details>

## Theory

### The simple version

Picture the dependencies as arrows between sub-tasks. At any point, some sub-tasks have every arrow pointing *into* them already satisfied (everything they depend on has already run) — those are the ones eligible to go next. Among the eligible ones, pick whichever was listed earliest in the original order; run it; that might free up new sub-tasks to become eligible; repeat until everything's scheduled.

### Why the tie-break exists at all

Without it, "a valid order" is underspecified — many different orders can all correctly respect every dependency, and a grader (or two people implementing this independently) would disagree on what "the" answer is. Anchoring ties to the original list order gives one specific, checkable answer while still leaving the interesting part (actually respecting dependencies) as the real test.

### How this shows up in real systems

This is exactly the algorithm behind build systems, task schedulers, and CI pipeline dependency graphs — anything with a `depends_on` relationship between units of work needs precisely this: find a valid execution order, deterministically, from a dependency graph. An agent planner decomposing a goal into an ordered sub-task list is doing this same job, just with "sub-tasks" instead of "build targets."

## Explanation

The function tracks two pieces of state built once up front: `dependents` (for each sub-task, which other sub-tasks list it as a `before`) and `indegree` (for each sub-task, how many not-yet-scheduled dependencies still block it). The main loop repeatedly finds the first sub-task, in original list order, whose `indegree` has reached zero — `next(s for s in subtasks if s in remaining and indegree[s] == 0)` does exactly this scan, naturally respecting the tie-break since it walks the original list in order and stops at the first eligible match. Scheduling that sub-task removes it from `remaining` and decrements the `indegree` of everything that depended on it, potentially making new sub-tasks eligible for the next iteration. Because the dependency graph is guaranteed acyclic, this process is guaranteed to make progress every iteration until every sub-task has been placed.
