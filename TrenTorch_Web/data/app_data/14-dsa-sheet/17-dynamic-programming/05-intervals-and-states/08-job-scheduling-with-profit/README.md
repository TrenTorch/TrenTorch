---
name: sheet-job-scheduling-with-profit
title: 'Weighted Job Scheduling'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Advanced
theory: job-scheduling-with-profit
---

## Statement

Each job is `[start, end, profit]` with `start < end`. You can do one job at a time; a job that **ends at time `t`** does not overlap one that **starts at `t`**. Return the **largest total profit** from a set of non-overlapping jobs.

For `[[1, 3, 50], [2, 4, 10], [3, 5, 40], [3, 6, 70]]` the answer is `120` (jobs 1 and 4).

The starter code scans backwards through all earlier jobs for each job. It is correct but too slow for many jobs.

### Examples

**Example 1**

Input:

```python
job_scheduling([[1, 3, 50], [2, 4, 10], [3, 5, 40], [3, 6, 70]])
```

Output:

```text
120
```

**Example 2**

Input:

```python
job_scheduling([[1, 2, 5], [1, 2, 6]])
```

Output:

```text
6
```

### Constraints

- `0 <= len(jobs) <= 100000`
- `1 <= start < end <= 10**9`
- `1 <= profit <= 10000`

## Explanation

`ends` is the sorted list of end times. `bisect_right(ends, start)` counts the jobs that end at or before `start`, which is the number of jobs available to precede this one.

### Complexity

- Time: O(n log n). Sort by end time, then one binary search per job.
- Space: O(n). The sorted list and the table.
