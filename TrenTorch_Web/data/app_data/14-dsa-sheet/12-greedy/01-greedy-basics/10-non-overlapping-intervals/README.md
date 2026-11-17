---
name: sheet-non-overlapping-intervals
title: 'Remove Overlapping Intervals'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Intermediate
theory: removing-the-fewest-intervals
---

## Statement

`intervals[i] = [start, end]`. Return the **fewest intervals to remove** so that the rest do **not overlap**. Intervals that only touch (one ends where the next starts) do not overlap.

For `[[1, 2], [2, 3], [3, 4], [1, 3]]` the answer is `1` (remove `[1, 3]`).

The starter code builds the longest chain with a double loop. It is correct but too slow for many intervals.

### Examples

**Example 1**

Input:

```python
erase_overlap([[1, 2], [2, 3], [3, 4], [1, 3]])
```

Output:

```text
1
```

**Example 2**

Input:

```python
erase_overlap([[1, 2], [1, 2], [1, 2]])
```

Output:

```text
2
```

### Constraints

- `0 <= len(intervals) <= 200000`
- `0 <= start < end <= 10**9`

## Explanation

`last_end` is the end of the last kept interval. An interval that starts earlier than that overlaps it and is removed.

### Complexity

- Time: O(n log n). Sorting by end time dominates; the scan is one pass.
- Space: O(n). The sorted list.
