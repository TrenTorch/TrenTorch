---
name: sheet-merge-intervals
title: 'Merge Intervals'
tags: [dsa-sheet, arrays, hard-arrays]
difficulty: Intermediate
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

## Theory

After **sorting by start**, any interval that overlaps the previous merged one must start at or before the previous end, and the intervals that follow only need to be compared with the **last merged interval**. So one sweep suffices.

Keep a list of merged intervals. For the next interval `[s, e]`: if `s <= last_end`, it overlaps the last merged interval, so extend `last_end = max(last_end, e)` (the new one might end earlier than the last, when it sits inside). Otherwise it starts a new merged interval.

The sort dominates: `O(n log n)`. Without the sort you would have to compare every pair.

## Explanation

`sorted(intervals)` orders by start then end. For each `[start, end]`, if `out` is not empty and `start <= out[-1][1]` the two overlap or touch, so raise the last end to `max(out[-1][1], end)`. Otherwise append a new interval. The interval lists are copied into new lists so the input is not modified.
