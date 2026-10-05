---
name: research-hugginggpt-topo-order
title: 'HuggingGPT: Ordering the Subtasks'
tags: [research-papers, agents, planning, orchestration]
difficulty: Advanced
---

## Statement

### The problem, from first principles

HuggingGPT (Shen et al., 2023) uses a language model to plan a set of subtasks, each handled by a specialist model. The subtasks form a dependency graph, and they must run in an order where each task's inputs are ready.

### From theory to code

Implement `topo_order(tasks)`, returning an execution order consistent with the dependencies, or None if the plan has a cycle.

### Constraints

- Break ties by task id so the order is deterministic.

### Hints

<details>
<summary>Hint 1</summary>

Repeatedly run a task whose dependencies are all finished. Track how many dependencies each task still waits on, and stop with None if some task never becomes ready.

</details>

## Theory

### The simple version

A valid order is what lets the orchestrator feed each specialist the outputs it needs. A cycle means the plan can never finish, which should be reported instead of executed.

### The formula

$$\text{for every edge } u \to v:\quad \operatorname{pos}(u) < \operatorname{pos}(v)$$

### How NumPy/PyTorch actually implements this

Workflow engines use topological sorts to schedule tasks with dependencies.

## Explanation

Kahn's algorithm is the standard method; sorting the ready queue makes the output reproducible.
