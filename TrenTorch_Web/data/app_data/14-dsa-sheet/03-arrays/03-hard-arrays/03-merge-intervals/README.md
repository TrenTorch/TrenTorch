---
name: sheet-merge-intervals
title: 'Merge Intervals'
tags: [dsa-sheet, arrays, hard-arrays]
difficulty: Intermediate
theory: merging-overlapping-intervals
---

## Statement

Each interval is `[start, end]` with `start <= end`. Merge every group of intervals that **overlap or touch** (for example `[1, 3]` and `[3, 5]` touch at `3`) into one interval, and return the merged intervals sorted by start. Intervals that only come close without touching (`[1, 2]` and `[3, 4]`) stay separate.

### Examples

**Example 1**

Input:

```python
merge_intervals([[1, 3], [8, 10], [2, 6], [15, 18]])
```

Output:

```text
[[1, 6], [8, 10], [15, 18]]
```

`[1, 3]` and `[2, 6]` overlap and merge into `[1, 6]`.

**Example 2**

Input:

```python
merge_intervals([[1, 4], [4, 5]])
```

Output:

```text
[[1, 5]]
```

They touch at 4, so they merge into `[1, 5]`.

### Constraints

- `0 <= len(intervals) <= 2 * 10**5`
- `0 <= start <= end <= 10**9`
- The intervals are in any order.

## Explanation

`sorted(intervals)` orders by start then end. For each `[start, end]`, if `out` is not empty and `start <= out[-1][1]` the two overlap or touch, so raise the last end to `max(out[-1][1], end)`. Otherwise append a new interval. The interval lists are copied into new lists so the input is not modified.

### Complexity

- Time: O(n log n). Sorting dominates; the merge itself is one pass.
- Space: O(n). The sorted list and the merged result.
