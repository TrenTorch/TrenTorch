---
name: production-ml-training-pipelines-dag
title: 'Training Pipelines: Turning a Notebook Into a Reproducible, Scheduled DAG'
tags: [mlops]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A notebook's cells run in whatever order you happen to click "run" — every dependency between steps (train can't run before featurize, which can't run before clean_data) exists only implicitly, in the author's head. The moment that pipeline needs to run unattended, on a schedule, reliably, every one of those implicit dependencies has to become an EXPLICIT graph: a DAG (Directed Acyclic Graph), where a scheduler can compute a valid execution order automatically — and detect, before ever running anything, if the dependencies as written don't actually make sense.

### From theory to code

Implement `add_task` (registering a task and its explicit dependencies), `topological_order` (computing a valid execution order via Kahn's algorithm), and `has_cycle`.

### Constraints

- `add_task(dag, task_name, depends_on)` records which tasks must run BEFORE the given task.
- `topological_order(dag)` returns a list where every task appears AFTER all of its dependencies; raises `ValueError` if the DAG contains a cycle.
- Ties (multiple tasks simultaneously ready to run) are broken alphabetically, for a fully deterministic result.
- `has_cycle(dag)` returns `True` exactly when `topological_order` would raise.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Kahn's algorithm: track each task's "in-degree" (how many un-run dependencies it still has). Start with every ZERO-in-degree task in a queue; whenever a task finishes, decrement its dependents' in-degrees, enqueueing any that just hit zero.

</details>

<details>
<summary>Hint 2</summary>

If the algorithm finishes but the output list is SHORTER than the total number of tasks, some tasks never reached in-degree zero — which can only happen if they're stuck in a cycle, waiting on each other forever.

</details>

## Theory

### The simple version

Imagine a recipe written as a flowchart instead of a numbered list: "knead dough" has an arrow pointing to it FROM "mix ingredients", and "bake" has arrows pointing to it from BOTH "knead dough" AND "preheat oven" — a valid way to actually cook the recipe is any ordering that respects every arrow, and there might be several equally valid orderings (preheating the oven could happen anytime before baking). But if someone accidentally drew an arrow from "bake" back to "mix ingredients," the flowchart would be nonsensical — there'd be no way to start at all. A DAG's cycle check is exactly this sanity check, done automatically.

### The formula

```text
topological_order (Kahn's algorithm):
    in_degree[task] = number of dependencies task still has
    queue = all zero-in-degree tasks (sorted, for determinism)
    while queue is not empty:
        task = queue.pop_front()
        order.append(task)
        for each dependent of task:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0: queue.push(dependent, sorted)
    if len(order) < total task count: raise ValueError  -- a cycle exists

has_cycle(dag) = "does topological_order(dag) raise?"
```

A genuinely valid DAG can have MULTIPLE correct topological orders (any order respecting the arrows counts) — this exercise's deterministic tie-breaking rule (alphabetical) exists purely so the exercise's own tests can check for one exact, reproducible answer, not because real schedulers care about alphabetical order specifically.

### How PyTorch actually implements this

Context only, untested by your submission: this is exactly the underlying model real ML orchestration tools use — Apache Airflow's DAGs, Kubeflow Pipelines, and Prefect flows all represent a training pipeline as an explicit graph of tasks and their dependencies, computing a valid execution order (and often running independent branches in parallel) using the same fundamental topological-sort idea this exercise implements from scratch.

## Explanation

`add_task` records a task's explicit dependency list directly — the entire point being that nothing about execution order is ever implied by, say, the order tasks happen to be added in.

`topological_order` runs Kahn's algorithm precisely: seed the queue with dependency-free tasks, repeatedly process the queue, and detect an unresolvable cycle by comparing the final output's length against the total task count — `tests.py` confirms correct behavior on linear chains, a genuinely branching "diamond" dependency structure (where two independent branches must both complete before a shared downstream task), and a deliberately deterministic tie-breaking case, plus its final oracle test confirms the function RAISES on a real cycle rather than silently returning a partial, dangerously incomplete order.

`has_cycle` is built directly on top of `topological_order` rather than reimplementing cycle detection separately, keeping the two functions' behavior automatically consistent with each other.
