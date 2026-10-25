---
name: sheet-job-scheduling-with-profit
title: 'Weighted Job Scheduling'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Advanced
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

**Explanation:** Jobs [1,3,50] and [3,6,70] end and start at the same time t=3 so they don't overlap. Their profits 50+70=120 are maximal among all non-overlapping subsets.

**Example 2**

Input:

```python
job_scheduling([[1, 2, 5], [1, 2, 6]])
```

Output:

```text
6
```

**Explanation:** Both jobs occupy identical interval [1,2] so only one can be chosen. The one with profit 6 yields the maximum total.

### Constraints

- `0 <= len(jobs) <= 100000`
- `1 <= start < end <= 10**9`
- `1 <= profit <= 10000`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

This is activity selection with **weights**, so greedy by end time no longer works. Sort the jobs by **end time**. **State:** `best[i]`, the largest profit using only the first `i` jobs in that order. **Transition:** job `i` is skipped (`best[i - 1]`) or taken, which adds its profit to the best result among the jobs that **end before it starts**: `best[i] = max(best[i - 1], profit + best[last_compatible])`.

The last compatible job is found by **binary search** on the sorted end times (`bisect_right(ends, start)`). `O(n log n)`.

## Explanation

`ends` is the sorted list of end times. `bisect_right(ends, start)` counts the jobs that end at or before `start`, which is the number of jobs available to precede this one.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                       | Variables                                                         |
| ----------------------------------------------------- | ----------------------------------------------------------------- |
| `items = sorted(jobs, key=lambda j: j[1])`            | `items = [[1, 3, 50], [2, 4, 10], [3, 5, 40], [3, 6, 70]]`        |
| `best = [0] * (len(items) + 1)`                       | `ends = [3, 4, 5, 6], best = [0, 0, 0, 0, 0]`                     |
| `before = bisect_right(ends, start, 0, i - 1)`        | `i = 1, start = 1, end = 3, profit = 50, before = 0`              |
| `for i, (start, end, profit) in enumerate(items, 1):` | `best = [0, 50, 0, 0, 0], i = 2, start = 2, end = 4, profit = 10` |
| `best[i] = max(best[i - 1], profit + best[before])`   | `best = [0, 50, 50, 0, 0]`                                        |
| `before = bisect_right(ends, start, 0, i - 1)`        | `i = 3, start = 3, end = 5, profit = 40, before = 1`              |
| `for i, (start, end, profit) in enumerate(items, 1):` | `best = [0, 50, 50, 90, 0], i = 4, end = 6, profit = 70`          |
| `return`                                              | `returned = 120`                                                  |

### Complexity

- Time: O(n log n) where n is number of jobs and q is 0.
- Extra space: O(n) where n is number of jobs and q is 0.
- The brute force takes O(2^n * n) where n is number of jobs and q is 0.
