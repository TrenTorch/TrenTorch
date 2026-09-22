---
name: agentic-learning-store-trajectories
title: Store Successful and Failed Agent Trajectories
tags: [agentic-systems, agent-learning, experience]
difficulty: Beginner
---

## Statement

### The problem, from first principles

An agent that never looks back at what it's already done can't get better over time — the raw material for improvement is a record of what was tried and whether it worked. The first, most basic step toward learning from experience isn't anything clever: it's simply separating what happened into "this worked" and "this didn't," so later questions in this track (retrieving similar past runs, extracting lessons from failures) have something real to draw from.

### From theory to code

You're given every trajectory's id and whether it succeeded, in order. Implement `classify_and_store(trajectories)`. Split them into two lists: ids of successful trajectories and ids of failed ones, each preserving the original relative order.

Return `(successful_ids, failed_ids)`.

### Constraints

- 0 to 1000 trajectories; ids need not be unique.

### Hints

<details>
<summary>Hint 1</summary>

Two independent list comprehensions, each filtering on the same `success` flag in opposite directions, is the entire solution — there's no need for a single combined loop with manual appending to two separate lists.

</details>

<details>
<summary>Hint 2</summary>

"Preserving relative order" just means: don't sort, don't reverse, don't group by anything other than the success flag. A straightforward filter over the original list already keeps everything in its original relative position.

</details>

## Theory

### The simple version

Walk the trajectory list once (conceptually — two comprehensions over the same list is fine too), and file each trajectory's id into one of exactly two buckets based on one boolean flag. Nothing more sophisticated than that.

### Why this trivial step matters

Every later question in this track — finding trajectories similar to a new task, reusing a plan that worked before, extracting a lesson from a failure — depends on already having successes and failures cleanly separated. Skipping straight to "clever" retrieval or lesson-extraction logic without this basic partition first would mean re-deriving success/failure status inside every later function instead of once, here, where it belongs.

### How this shows up in real systems

Any system that learns from its own history needs exactly this kind of basic bookkeeping as its foundation — a trajectory store, an experience replay buffer, a training-data curation pipeline all start by separating "worked" from "didn't" before any more sophisticated retrieval, ranking, or lesson-extraction logic gets layered on top.

## Explanation

The function computes two independent list comprehensions over the same `trajectories` list: one keeping only the ids where `success` is true, the other keeping only the ids where it's false. Because each comprehension walks `trajectories` in its original order and only ever filters (never reorders or groups), both resulting lists preserve the relative order the matching trajectories originally appeared in — a trajectory earlier in the input list that belongs to a given bucket always appears before a later trajectory in that same bucket.
