---
name: sheet-max-consecutive-ones
title: 'Longest Run of Ones'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Beginner
---

## Statement

`nums` contains only `0` and `1`. Return the length of the longest run of **consecutive** `1`s. If there are no `1`s, return `0`.

### Examples

**Example 1**

Input:

```python
max_consecutive_ones([1, 1, 0, 1, 1, 1])
```

Output:

```text
3
```

**Example 2**

Input:

```python
max_consecutive_ones([0, 0])
```

Output:

```text
0
```

### Constraints

- `0 <= len(nums) <= 3 * 10**5`
- Every value is `0` or `1`.

## Theory

Keep a running count of the current run. A `1` extends it; a `0` ends it, so reset the count. After each step remember the best count seen.

This "current vs best" pair appears in many array problems (it is also the heart of Kadane's algorithm). The key habit is updating `best` **inside** the loop, because a run can end at the last element with no `0` after it to trigger a check.

## Explanation

`current` counts the ones in the run that is being read. On `1` add one and update `best`; on `0` set `current` back to zero.
