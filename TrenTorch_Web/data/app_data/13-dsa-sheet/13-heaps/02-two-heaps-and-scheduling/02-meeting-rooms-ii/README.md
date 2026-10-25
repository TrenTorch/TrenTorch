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

**Explanation:** Two rooms are needed because [0,30] overlaps both [5,10] and [15,20], but [5,10] ends before [15,20] starts, so one room handles the first two, another the third.

**Example 2**

Input:

```python
min_meeting_rooms([[7, 10], [2, 4]])
```

Output:

```text
1
```

**Explanation:** Only one room because intervals do not overlap; [2,4] ends before [7,10] starts.

### Constraints

- `0 <= len(meetings) <= 100000`
- `0 <= start < end <= 10**9`

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

Process the meetings in order of **start time**. Keep a min-heap of the **end times of the rooms currently in use**. For a new meeting: if the room that frees up the earliest (the heap top) is already free (`end <= start`), **reuse it** (pop it); then push this meeting's end time. The size of the heap at its largest is the number of rooms needed.

Each meeting costs `O(log n)`, plus the sort: `O(n log n)` overall. Compare with the earlier "minimum platforms" question, which solved the same problem by sorting starts and ends separately.

## Explanation

`rooms` holds end times. Reusing a room means replacing its end time with the new one, so the heap grows only when no room is free.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                       | Variables              |
| ------------------------------------- | ---------------------- |
| `rooms = []`                          | `rooms = []`           |
| `for start, end in sorted(meetings):` | `start = 0, end = 30`  |
| `heapq.heappush(rooms, end)`          | `rooms = [30]`         |
| `for start, end in sorted(meetings):` | `start = 5, end = 10`  |
| `heapq.heappush(rooms, end)`          | `rooms = [10, 30]`     |
| `for start, end in sorted(meetings):` | `start = 15, end = 20` |
| `heapq.heapreplace(rooms, end)`       | `rooms = [20, 30]`     |
| `return`                              | `returned = 2`         |

### Complexity

- Time: O(n log n) sorting, n is number of meetings.
- Extra space: O(n) for heap of active ends.
- The brute force takes O(n^2) counting overlaps per meeting.
