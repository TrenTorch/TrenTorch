---
name: research-voyager-next-task
title: 'Voyager: Choosing the Next Task'
tags: [research-papers, agents, embodied, skill-library]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Voyager's automatic curriculum proposes the next task based on what the agent has already done. The simplest version walks the proposed tasks in order and skips completed ones.

### From theory to code

Implement `next_task(done, candidates)`, returning the first unfinished candidate.

### Constraints

- Return None if every candidate is done.

### Hints

<details>
<summary>Hint 1</summary>

Scan the candidates in order and return the first not present in the done set.

</details>

## Theory

### The simple version

A curriculum keeps the agent on tasks that are slightly beyond its current skills. Skipping completed work is the minimal form of that progression.

### The formula

$$t^* = \min_{\text{order}}\{\,t \in C : t \notin D\,\}$$

### How NumPy/PyTorch actually implements this

Voyager's curriculum prompts the LLM with the completed tasks; this filter is the deterministic part of that loop.

## Explanation

The function is a pure selection over an ordered list, which makes the curriculum easy to test.
