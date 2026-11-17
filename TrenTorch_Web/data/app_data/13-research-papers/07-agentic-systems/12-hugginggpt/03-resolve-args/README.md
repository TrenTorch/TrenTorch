---
name: research-hugginggpt-resolve-args
title: 'HuggingGPT: Resolving Task Placeholders'
tags: [research-papers, agents, planning, orchestration]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

In HuggingGPT, later subtasks refer to earlier outputs by placeholder, for example the image produced by task 1. Before a subtask runs, those placeholders are replaced with the actual values.

### From theory to code

Implement `resolve_args(args, results)`, substituting each placeholder with its task output.

### Constraints

- Placeholders look like `<task_id>`.

### Hints

<details>
<summary>Hint 1</summary>

For each completed task, replace its placeholder text with the string form of its result.

</details>

## Theory

### The simple version

Substitution is how data flows between specialist models. Placeholders that do not match a completed task are left untouched so the error stays visible.

### The formula

$$\text{args}' = \text{args}[\,\langle t\rangle \mapsto \text{str}(r_t)\,]_{t \in \text{done}}$$

### How NumPy/PyTorch actually implements this

Orchestrators perform this substitution right before invoking each tool.

## Explanation

Only completed tasks are substituted, so a dependency that has not run yet still shows up as a placeholder.
