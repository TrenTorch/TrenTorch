---
name: agentic-parallel-stages
title: Parallel Stages & Critical Path
tags: [agentic-systems, planning, workflows, parallelism]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Tasks that do not depend on each other can run at the same time, and an agent that runs independent tool calls in parallel finishes much sooner. Grouping a DAG into **stages** makes this explicit: stage 0 holds tasks with no dependencies, stage 1 holds tasks whose dependencies are all in stage 0, and so on, so every task in a stage can run concurrently. How fast the whole plan can possibly finish is limited by the **critical path**, the longest chain of dependent tasks measured by duration. No amount of parallel hardware beats it, so it tells you which task to speed up first.

### From theory to code

Implement `parallel_stages` and `critical_path_length`.

### Constraints

- `tasks` maps each task to its dependency list and is guaranteed to be a valid DAG.
- `parallel_stages(tasks)` returns a list of stages. A task's stage index is `0` if it has no dependencies, else `1 + max(stage of its dependencies)`. Each stage is a list of task names sorted alphabetically; stages are in increasing order.
- `critical_path_length(tasks, durations)` is the largest total duration over all dependency chains, where `durations[name]` is the time of that task. Return a float (`0.0` for an empty plan).

### Hints

<details>
<summary>Hint 1</summary>

Compute each task's stage (and its earliest finish time) with memoized recursion over the dependencies.

</details>

<details>
<summary>Hint 2</summary>

The critical path is the maximum earliest-finish time over all tasks.

</details>

## Theory

### The simple version

Building a house: plumbing and electrical can happen together, but both must finish before the walls close. The longest chain of must-follow steps sets the minimum build time.

### The formula

$$
\text{stage}(v) = \begin{cases} 0 & \text{no deps}\\ 1 + \max_{u \in \text{deps}(v)} \text{stage}(u) & \text{otherwise}\end{cases}, \qquad
f(v) = d_v + \max_{u \in \text{deps}(v)} f(u), \quad \text{CP} = \max_v f(v)
$$

### How this is done in practice

LLM compilers and agent frameworks use this to fan out independent tool calls (LLMCompiler) and to schedule sub-agents. In project management the same computation is the critical path method.

## Explanation

Both quantities are longest-path computations on a DAG, one in hops and one in time. A shared memoized recursion computes them, and each test targets one property.
