---
name: agentic-replan-after-failure
title: Replanning After Failure
tags: [agentic-systems, planning, recovery, workflows]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Plans meet reality. A step fails because a tool is down, a page does not load or an API refuses the request, and a robust agent does not start over or give up. It **replans**: keep everything already done, replace the failed step's tool with a fallback, and continue with the rest. The remaining steps that depended on completed work no longer need those dependencies, because the results already exist. Implementing this as a pure function on plan data makes the recovery logic testable without running any tools.

### From theory to code

Implement `replan`.

### Constraints

- `plan` is a list of step dicts with keys `id`, `tool` and `depends_on`. `completed` is a set of finished step ids, `failed_id` is the id of the step that failed and `fallbacks` maps a tool name to its fallback tool name.
- Return a **new** plan containing, in the original order, every step whose id is not in `completed`. The failed step's `tool` is replaced by `fallbacks[tool]`; if it has no fallback, raise `ValueError`.
- In the returned steps, remove from `depends_on` every id in `completed`. Other fields are kept unchanged.
- `failed_id` must not be in `completed`. Do not modify the input plan.

### Hints

<details>
<summary>Hint 1</summary>

Copy each remaining step (`dict(step)`) before changing it, and build a new `depends_on` list.

</details>

<details>
<summary>Hint 2</summary>

Only the failed step changes its tool; later steps keep theirs.

</details>

## Theory

### The simple version

A road trip with a closed bridge: you keep the miles already driven, take a detour for that leg and carry on, no longer worrying about the earlier towns you have passed.

### The formula

$$
\text{plan}' = \big[\, s'_i : s_i \in \text{plan},\ \text{id}_i \notin C \,\big], \qquad
\text{deps}'_i = \text{deps}_i \setminus C, \qquad \text{tool}'_{f} = \phi(\text{tool}_f)
$$

### How this is done in practice

Plan-and-execute agents (LangGraph, AutoGen) use a replanner node. Real systems also record why the step failed and prefer fallbacks ranked by cost, and escalate to the user when no fallback remains.

## Explanation

The function is a filter plus a controlled edit of one element. Returning copies is what makes it safe to keep the old plan for logging and comparison.
