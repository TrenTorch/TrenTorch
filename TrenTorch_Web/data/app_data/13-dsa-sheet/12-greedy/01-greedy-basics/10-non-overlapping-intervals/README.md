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

**Explanation:** The greedy algorithm removes intervals that overlap with the current non-overlapping chain. In this case, [1, 3] overlaps [1, 2] and [2, 3], so it is removed to maintain a non-overlapping sequence.

**Example 2**

Input:

```python
erase_overlap([[1, 2], [1, 2], [1, 2]])
```

Output:

```text
2
```

**Explanation:** Since all intervals are identical and overlapping, the greedy algorithm will remove all but the first one, resulting in two removed intervals.

### Constraints

- `0 <= len(intervals) <= 200000`
- `0 <= start < end <= 10**9`

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

Removing the fewest intervals means **keeping the most**: this is exactly activity selection. Sort by **end time**, keep an interval if it starts at or after the end of the last kept one, and count the ones you skip. The skipped ones are the removals.

The exchange argument is the same: the interval that ends first leaves the most room for the others.

## Explanation

`last_end` is the end of the last kept interval. An interval that starts earlier than that overlaps it and is removed.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                              | Variables                          |
| ------------------------------------------------------------ | ---------------------------------- |
| `removed = 0`                                                | `removed = 0`                      |
| `last_end = None`                                            | `last_end = None`                  |
| `last_end = end`                                             | `last_end = 2, start = 1, end = 2` |
| `for start, end in sorted(intervals, key=lambda it: it[1]):` | `start = 2, end = 3`               |
| `for start, end in sorted(intervals, key=lambda it: it[1]):` | `last_end = 3, start = 1`          |
| `removed += 1`                                               | `removed = 1`                      |
| `last_end = end`                                             | `last_end = 4, start = 3, end = 4` |
| `return`                                                     | `returned = 1`                     |

### Complexity

- Time: O(n log n) due to the initial sorting of intervals by end time, followed by a linear sweep to identify overlaps.
- Extra space: O(n) for the sorted list of intervals. The removal count is stored in a constant-space integer variable.
- The brute force takes O(2^n * n log n) because it explores every possible subset of intervals (2^n) and sorts each subset (n log n) to check for overlaps.
