---
name: agentic-learning-experience-based-planning
title: Experience-Based Planning From Past Runs
tags: [agentic-systems, agent-learning, planning]
difficulty: Beginner
---

## Statement

### The problem, from first principles

If an agent has already run a plan for this *exact* task before and it worked well, re-deriving a plan from scratch is wasted effort — the cheapest, most reliable plan is often just "do what worked last time." This is the simplest possible form of experience-based planning: not a general similarity search (that's the previous question's job), just a direct lookup for an exact repeat of a task the agent has already solved.

### From theory to code

You're given `query_task` (the exact task being planned for right now) and `past_plans` — `(task_name, plan, success_rate)` for every past run logged, in order. Implement `pick_best_past_plan(query_task, past_plans)`. Among entries whose `task_name` **exactly** matches `query_task`, return the `plan` with the highest `success_rate` (ties broken by whichever was seen first in `past_plans`). Return `None` if no past plan exists for this exact task.

### Constraints

- 0 to 500 past plans; `success_rate` is a real number in `[0, 1]`.

### Hints

<details>
<summary>Hint 1</summary>

This is a filtered argmax: only consider entries whose `task_name` exactly matches, and among those, track the one with the highest `success_rate` seen so far as you scan.

</details>

<details>
<summary>Hint 2</summary>

Use a strict `>` comparison (not `>=`) when updating the best-so-far — that's what makes the *first* occurrence of the maximum win a tie, rather than the last.

</details>

## Theory

### The simple version

Scan the history once, ignore anything whose task name doesn't match exactly, and keep track of the best-performing plan among what's left. If nothing matches at all, there's no experience to reuse — return `None` and let the caller fall back to planning from scratch.

### Why exact match, not "similar task"

Reusing a plan wholesale only makes sense when the task is genuinely the same one, not merely related — a plan for "book a domestic flight" might be actively wrong for "book an international flight" (different documents, different steps), even though the tasks sound similar. Exact-match reuse is deliberately conservative: it only fires when there's real, hard evidence this precise task has already been solved before, leaving the fuzzier "is this similar enough to help" question to a different mechanism (see the tag-overlap retrieval in the previous question).

### How this shows up in real systems

Caching a known-good solution for an exact repeat request is one of the cheapest, highest-value forms of "learning from experience" a system can implement — before reaching for anything more sophisticated (similarity search, learned re-ranking), checking "have I solved this literal task before, and how well did it go" is often enough to skip re-planning entirely for a large fraction of real repeat traffic.

## Explanation

The function scans `past_plans` once, keeping a running `best_plan` and `best_rate` (initialized below any real success rate). For each entry, it only updates the running best when the task name matches `query_task` exactly **and** the entry's `success_rate` strictly exceeds the current best — the strict `>` comparison is what makes the first-seen entry win when two entries for the same task tie on success rate, since a later equal-rate entry never satisfies "strictly greater" against the one already recorded. If no entry ever matches `query_task` at all, `best_plan` never leaves its initial `None` and that's what gets returned.
