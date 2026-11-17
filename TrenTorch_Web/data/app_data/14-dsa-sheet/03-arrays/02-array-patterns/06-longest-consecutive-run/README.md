---
name: sheet-longest-consecutive-run
title: 'Longest Consecutive Sequence'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Intermediate
theory: a-set-for-neighbours-in-value
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

## Explanation

Build `s = set(nums)`. For each `x` in `s` with `x - 1 not in s`, extend `length` while `x + length in s`, then update the best. Iterating the set removes duplicates. The inner `while` runs only from run starts, which keeps the total linear.

### Complexity

- Time: O(n). Only the start of a run begins a scan, so every value is visited at most twice (O(1) hash lookups on average).
- Space: O(n). The set of values.
