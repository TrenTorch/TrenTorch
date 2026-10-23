---
name: sheet-job-sequencing
title: 'Job Sequencing With Deadlines'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Advanced
---

## Statement

Each job is `[deadline, profit]`. Every job takes **one unit of time**, you can do one job at a time, starting at time 1, and a job must **finish by its deadline** (a job with deadline `d` can be done in a time slot `1..d`). Return the **largest total profit**.

For `[[4, 20], [1, 10], [1, 40], [1, 30]]` the answer is `60` (the jobs with profit 40 and 20).

### Examples

**Example 1**

Input:

```python
max_job_profit([[4, 20], [1, 10], [1, 40], [1, 30]])
```

Output:

```text
60
```

**Example 2**

Input:

```python
max_job_profit([[2, 100], [1, 19], [2, 27], [1, 25], [1, 15]])
```

Output:

```text
127
```

### Constraints

- `0 <= len(jobs) <= 100000`
- `1 <= deadline <= 100000`
- `1 <= profit <= 10**4`

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

The most profitable job is always worth doing if it can be scheduled. So sort the jobs by **profit, highest first**. Put each job in the **latest free slot before its deadline**: the latest one, so the earlier slots stay open for jobs with tighter deadlines. If no slot is free, skip the job.

Finding the latest free slot by scanning down costs `O(deadline)`; a **union-find (disjoint set)** structure makes it nearly `O(1)`: `parent[t]` points to the next free slot at or below `t`. Used slots are linked to the slot below them.

## Explanation

`find(t)` returns the latest free slot `<= t` (`0` means none). After using slot `s`, `parent[s] = s - 1` so later searches skip it.
