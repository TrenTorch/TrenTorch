---
name: agentic-learning-compare-with-without-experience
title: Compare an Agent With and Without Experience
tags: [agentic-systems, agent-learning, evaluation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Building a whole experience-retrieval system (this track's earlier questions) is only worth it if it actually helps. Proving that requires a real A/B comparison: run the same set of tasks twice, once with the agent allowed to draw on past experience and once without, and measure the difference — not just "did it get better on average," but specifically which tasks experience actually rescued.

### From theory to code

You're given two same-length lists of per-task success (`True`/`False`), for the same tasks in the same order: `with_experience` and `without_experience`. Implement `compare_experience_impact(with_experience, without_experience)`. Compute:

- `"with_success_rate"`: fraction of tasks the with-experience agent succeeded on.
- `"without_success_rate"`: same, for the without-experience agent.
- `"tasks_only_with_helped"`: count of tasks where the with-experience agent succeeded **and** the without-experience agent failed on that same task.
- `"delta"`: `with_success_rate - without_success_rate`.

Return the dict with exactly these four keys.

### Constraints

- 1 to 1000 tasks; both lists always the same length.

### Hints

<details>
<summary>Hint 1</summary>

`sum(a_list_of_booleans) / len(...)` gives a success rate directly, since `True` counts as `1` and `False` as `0` in a sum — no need for an explicit count-then-divide loop.

</details>

<details>
<summary>Hint 2</summary>

`tasks_only_with_helped` is specifically about tasks where _only_ the with-experience agent succeeded — `zip` the two lists together and count positions where the with-experience value is `True` and the without-experience value is `False` for that exact same task, not just "count successes in each list separately."

</details>

## Theory

### The simple version

Four numbers, each a direct aggregate over the two result lists: how often each version succeeded overall, how much better (or worse) the with-experience version did on average, and — the most specific and useful number — exactly how many individual tasks experience flipped from a failure into a success.

### Why a per-task "only helped" count matters more than just the aggregate rates

Two aggregate success rates can tell you _that_ something changed, but not _where_. If experience helped on 40% of tasks but also introduced new failures on a different 10% (overconfidence from a bad past example, say), the aggregate rates alone would still show net improvement while hiding a real regression worth investigating. Counting tasks where with-experience succeeded specifically where without-experience failed on that _same_ task is what surfaces where the real, task-level benefit is actually happening.

### How this shows up in real systems

This is a standard ablation-study pattern: hold everything else constant, toggle one capability on and off, and measure both the aggregate effect and the task-level detail. It's exactly how a team would justify (or fail to justify) shipping a new experience-retrieval feature — a positive aggregate delta is necessary but not sufficient; understanding which specific cases actually benefited is what turns a number into an actionable finding.

## Explanation

Both success rates are computed the same way: `sum(results) / len(results)`, relying on Python treating `True` as `1` and `False` as `0` in a sum, so no explicit counting loop is needed for either aggregate. `tasks_only_with_helped` walks both lists together with `zip`, counting positions where the with-experience value is `True` and the without-experience value is `False` for that exact same task — using `zip` (rather than two separate `sum()` calls) is what correctly ties the comparison to _matching_ tasks rather than just comparing two independent totals. `delta` is a direct subtraction of the two already-computed rates, requiring no additional pass over the data.
