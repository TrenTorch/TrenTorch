---
name: sheet-activity-selection
title: 'Activity Selection'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Intermediate
theory: activity-selection
---

## Statement

Activity `i` runs from time `starts[i]` to time `ends[i]` (with `starts[i] < ends[i]`). You can attend only one activity at a time, and an activity that **ends at time `t`** does not overlap one that **starts at `t`**. Return the **largest number of activities** you can attend.

For `starts = [1, 3, 0, 5, 8, 5]` and `ends = [2, 4, 6, 7, 9, 9]` the answer is `4`.

### Examples

**Example 1**

Input:

```python
max_activities([1, 3, 0, 5, 8, 5], [2, 4, 6, 7, 9, 9])
```

Output:

```text
4
```

**Example 2**

Input:

```python
max_activities([1, 2], [3, 4])
```

Output:

```text
1
```

### Constraints

- `0 <= len(starts) == len(ends) <= 200000`
- `0 <= starts[i] < ends[i] <= 10**9`

## Explanation

`last_end` is the end of the last chosen activity. After sorting by end time, an activity is taken exactly when it starts at or after `last_end`.

### Complexity

- Time: O(n log n). Sorting by end time dominates; the selection is one pass.
- Space: O(n). The sorted list.
