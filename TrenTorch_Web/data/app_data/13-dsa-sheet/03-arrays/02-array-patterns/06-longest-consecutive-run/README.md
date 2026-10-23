---
name: sheet-longest-consecutive-run
title: 'Longest Consecutive Sequence'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Intermediate
---

## Statement

Return the length of the longest set of values in `nums` that are **consecutive whole numbers** such as `4, 5, 6, 7`. The values can appear anywhere and in any order, and repeats count once. An empty list gives `0`.

Sorting works in `O(n log n)`. See if you can do it in `O(n)`.

### Examples

**Example 1**

Input:

```python
longest_consecutive([100, 4, 200, 1, 3, 2])
```

Output:

```text
4
```

`1, 2, 3, 4` is the longest run.

**Example 2**

Input:

```python
longest_consecutive([5, 5, 5])
```

Output:

```text
1
```

Repeats count once.

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `-10**9 <= nums[i] <= 10**9`

## Theory

Sorting puts consecutive values next to each other, so one scan finds the longest run. To beat `O(n log n)`, use a `set` for instant membership checks.

The key idea is to only start counting at the **beginning** of a run. A value `x` begins a run when `x - 1` is **not** in the set. From such a value, count upward while `x + 1`, `x + 2`, ... are in the set. A value in the middle of a run is skipped, because its run is counted from the start.

Each value is visited as a start at most once and as a run member at most once, so the total work is `O(n)` even though there is a loop inside a loop.

## Explanation

Build `s = set(nums)`. For each `x` in `s` with `x - 1 not in s`, extend `length` while `x + length in s`, then update the best. Iterating the set removes duplicates. The inner `while` runs only from run starts, which keeps the total linear.
