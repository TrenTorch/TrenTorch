---
name: agentic-dag-execution-order
title: Workflow DAG Ordering
tags: [agentic-systems, planning, workflows, graphs]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

An agent that decomposes a goal produces tasks with dependencies: you cannot summarize search results before searching, and you cannot send the email before drafting it. Those dependencies form a **directed acyclic graph** (DAG), and an executor needs an order in which every task runs after everything it depends on, a **topological order**. The standard method, Kahn's algorithm, repeatedly takes a task whose dependencies are all done. Two things can go wrong in a plan written by a language model, and both must be detected: a task may depend on a name that does not exist, and the dependencies may form a cycle, in which case no valid order exists.

### From theory to code

Implement `execution_order`.

### Constraints

- `tasks` is a dict mapping each task name to the list of task names it depends on. Return a list of all task names in an order where every task appears after all of its dependencies.
- When several tasks are ready at once, run the one that comes **first alphabetically**, so the result is deterministic.
- Raise `ValueError` if a dependency names a task that is not a key of `tasks`, or if the dependencies contain a cycle.
- Do not modify `tasks`.

### Hints

<details>
<summary>Hint 1</summary>

Count unmet dependencies for each task, keep a pool of ready tasks, and pick the smallest name each time.

</details>

<details>
<summary>Hint 2</summary>

If the output has fewer tasks than the input, the remainder are on or behind a cycle.

</details>

## Theory

### The simple version

Cooking dinner: the sauce needs the tomatoes chopped, the plating needs the sauce. A valid order exists unless two steps wait for each other, which is a cycle.

### The formula

A topological order is a sequence $v_1, \dots, v_n$ such that for every edge $u \to v$ ($v$ depends on $u$), $u$ appears before $v$. One exists iff the graph has no directed cycle, and Kahn's algorithm finds it in $O(V + E)$.

### How this is done in practice

Workflow engines (Airflow, Prefect, LangGraph) build and execute exactly this graph. When an LLM writes the plan, validating it before execution catches hallucinated task names and circular dependencies cheaply, before any tool has been called.

## Explanation

The algorithm maintains in-degrees and a ready set. The deterministic tie-break matters for reproducible runs and for tests, and detecting the leftover tasks gives cycle detection for free.
