---
name: sheet-job-sequencing
title: 'Job Sequencing With Deadlines'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Advanced
theory: job-sequencing-with-deadlines
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

## Explanation

`find(t)` returns the latest free slot `<= t` (`0` means none). After using slot `s`, `parent[s] = s - 1` so later searches skip it.

### Complexity

- Time: O(n log n). Sorting by profit dominates; finding a free slot with union-find is almost O(1) per job.
- Space: O(n). The union-find array and the sorted list.
