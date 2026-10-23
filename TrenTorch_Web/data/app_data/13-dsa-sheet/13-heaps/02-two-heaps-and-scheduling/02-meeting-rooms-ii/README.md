---
name: sheet-meeting-rooms-ii
title: 'Meeting Rooms'
tags: [dsa-sheet, heaps, two-heaps-and-scheduling]
difficulty: Intermediate
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

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

Process the meetings in order of **start time**. Keep a min-heap of the **end times of the rooms currently in use**. For a new meeting: if the room that frees up the earliest (the heap top) is already free (`end <= start`), **reuse it** (pop it); then push this meeting's end time. The size of the heap at its largest is the number of rooms needed.

Each meeting costs `O(log n)`, plus the sort: `O(n log n)` overall. Compare with the earlier "minimum platforms" question, which solved the same problem by sorting starts and ends separately.

## Explanation

`rooms` holds end times. Reusing a room means replacing its end time with the new one, so the heap grows only when no room is free.
