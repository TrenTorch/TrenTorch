---
name: agentic-plan-validation
title: Plan Validation
tags: [agentic-systems, planning, validation, tools]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Language models write plans as structured data: a list of steps, each naming a tool, its arguments and the earlier steps it depends on. Before executing anything, a safe agent checks the plan against what is actually available, because models routinely invent tools that do not exist, omit required arguments, add arguments the tool does not accept and reference steps that come later or never. Catching these statically is cheap, and the error messages are valuable: returned to the model they let it repair its own plan.

### From theory to code

Implement `validate_plan`.

### Constraints

- `plan` is a list of dicts with keys `id`, `tool`, `args` (a dict) and `depends_on` (a list of step ids). `tools` maps tool name to `{'required': [...], 'optional': [...]}`.
- Check steps in plan order and return a list of error strings (empty if the plan is valid). For each step, in this order: if the tool is unknown, add `step {id}: unknown tool '{tool}'` and skip the argument checks; otherwise add `step {id}: missing argument '{a}'` for each required argument absent from `args` (alphabetical), then `step {id}: unexpected argument '{a}'` for each argument in neither list (alphabetical).
- Then, for each id in `depends_on` in the listed order: if it is not the id of an **earlier** step, add `step {id}: invalid dependency '{d}'`.
- Step ids are unique strings.

### Hints

<details>
<summary>Hint 1</summary>

Keep a set of the ids seen so far while iterating, so 'earlier step' is a set lookup.

</details>

<details>
<summary>Hint 2</summary>

A dependency on a later or unknown step is invalid for the same reason: it is not available yet.

</details>

## Theory

### The simple version

A building inspector reads the blueprint before any concrete is poured: does every named material exist, is every required measurement present and does each step only rely on work already done.

### The formula

A plan is valid iff for every step $s_i$: $\text{tool}(s_i) \in \mathcal{T}$, $\text{req}(\text{tool}) \subseteq \text{args}(s_i) \subseteq \text{req} \cup \text{opt}$, and $\text{deps}(s_i) \subseteq \{s_1, \dots, s_{i-1}\}$. The last condition makes the plan acyclic by construction.

### How this is done in practice

Function-calling APIs validate arguments against JSON Schema, and agent frameworks add a plan check before running. Feeding the exact error strings back to the model in a retry prompt is one of the most effective reliability tricks for tool use.

## Explanation

A single pass with a running set of seen ids. The ordering of error messages is fixed by the statement so that an agent loop can compare error lists exactly.
