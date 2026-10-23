---
name: sheet-non-overlapping-intervals
title: 'Remove Overlapping Intervals'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Intermediate
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

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

Removing the fewest intervals means **keeping the most**: this is exactly activity selection. Sort by **end time**, keep an interval if it starts at or after the end of the last kept one, and count the ones you skip. The skipped ones are the removals.

The exchange argument is the same: the interval that ends first leaves the most room for the others.

## Explanation

`last_end` is the end of the last kept interval. An interval that starts earlier than that overlaps it and is removed.
