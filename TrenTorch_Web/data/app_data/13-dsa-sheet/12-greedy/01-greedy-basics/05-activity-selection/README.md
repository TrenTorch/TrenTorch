---
name: sheet-activity-selection
title: 'Activity Selection'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Intermediate
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

**Explanation:** Activities sorted by finish time allow selection of four compatible activities: [1,2], [3,4], [5,7], [8,9].

**Example 2**

Input:

```python
max_activities([1, 2], [3, 4])
```

Output:

```text
1
```

**Explanation:** Only one activity can be chosen because both overlap; the algorithm selects the earlier ending activity, yielding count 1.

### Constraints

- `0 <= len(starts) == len(ends) <= 200000`
- `0 <= starts[i] < ends[i] <= 10**9`

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

Which activity should you attend first? Not the one that starts first, and not the shortest. The one that **ends first** is always safe: it leaves the most time free for everything else, so any best schedule can swap its first activity for the one that ends earliest without losing anything.

So: sort the activities by **end time**. Take the first; then repeatedly take the next one that starts at or after the end of the last taken. This is the classic example of an **exchange argument**: change an optimal answer step by step into the greedy one without making it worse.

## Explanation

`last_end` is the end of the last chosen activity. After sorting by end time, an activity is taken exactly when it starts at or after `last_end`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                | Variables                                     |
| ---------------------------------------------- | --------------------------------------------- |
| `count = 0`                                    | `count = 0`                                   |
| `for end, start in sorted(zip(ends, starts)):` | `last_end = -1, end = 2, start = 1`           |
| `for end, start in sorted(zip(ends, starts)):` | `count = 1, last_end = 2, end = 4, start = 3` |
| `last_end = end`                               | `count = 2, last_end = 4`                     |
| `for end, start in sorted(zip(ends, starts)):` | `end = 7, start = 5`                          |
| `last_end = end`                               | `count = 3, last_end = 7`                     |
| `count += 1`                                   | `count = 4, end = 9, start = 8`               |
| `return`                                       | `returned = 4`                                |
