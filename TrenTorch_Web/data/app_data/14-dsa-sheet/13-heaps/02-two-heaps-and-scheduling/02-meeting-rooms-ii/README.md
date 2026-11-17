---
name: sheet-meeting-rooms-ii
title: 'Meeting Rooms'
tags: [dsa-sheet, heaps, two-heaps-and-scheduling]
difficulty: Intermediate
theory: which-room-is-free-first
---

## Statement

Each meeting is `[start, end]` (with `start < end`). A meeting that **ends at time `t`** does not conflict with one that **starts at `t`**. Return the **fewest rooms** needed to hold all the meetings.

For `[[0, 30], [5, 10], [15, 20]]` the answer is `2`.

The starter code counts the running meetings at every start time. It is correct but too slow for many meetings.

### Examples

**Example 1**

Input:

```python
min_meeting_rooms([[0, 30], [5, 10], [15, 20]])
```

Output:

```text
2
```

**Example 2**

Input:

```python
min_meeting_rooms([[7, 10], [2, 4]])
```

Output:

```text
1
```

### Constraints

- `0 <= len(meetings) <= 100000`
- `0 <= start < end <= 10**9`

## Explanation

`rooms` holds end times. Reusing a room means replacing its end time with the new one, so the heap grows only when no room is free.

### Complexity

- Time: O(n log n). Sorting by start time dominates; the heap holds room end times, `O(log n)` per meeting.
- Space: O(n). The heap and the sorted list.
