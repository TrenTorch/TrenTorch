---
name: research-hugginggpt-valid-plan
title: 'HuggingGPT: Checking a Plan'
tags: [research-papers, agents, planning, orchestration]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Before HuggingGPT runs a plan, it has to be well formed: every referenced task exists and the dependencies do not loop. Rejecting a bad plan early avoids running part of it and then failing.

### From theory to code

Implement `is_valid_plan(tasks)`, returning whether the plan can be executed.

### Constraints

- A task that depends on itself is a cycle.

### Hints

<details>
<summary>Hint 1</summary>

First check that every dependency is a known task. Then check the graph is acyclic by counting how many tasks a dependency-respecting pass can reach.

</details>

## Theory

### The simple version

Validation before execution turns a runtime failure into a clear planning error, which the model can be asked to repair.

### The formula

$$\text{valid} \iff \text{deps}(t) \subseteq \text{tasks} \;\land\; \text{the graph is a DAG}$$

### How NumPy/PyTorch actually implements this

Plan validators in orchestration frameworks run the same two checks before dispatching work.

## Explanation

The reachability count is equivalent to Kahn's algorithm finishing with all tasks scheduled.
