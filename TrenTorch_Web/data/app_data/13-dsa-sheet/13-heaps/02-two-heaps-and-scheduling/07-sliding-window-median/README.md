---
name: sheet-sliding-window-median
title: 'Sliding Window Median'
tags: [dsa-sheet, heaps, two-heaps-and-scheduling]
difficulty: Mastery
---

## Statement

A window of size `k` slides over `nums` one position at a time. Return the **median of each window**: the middle value for an odd `k`, or the average of the two middle values for an even `k`, as decimals.

For `nums = [1, 3, -1, -3, 5, 3, 6, 7]` and `k = 3` the answer is `[1.0, -1.0, -1.0, 3.0, 5.0, 6.0]`.

The starter code sorts every window from scratch. It is correct but too slow when windows are large.

### Examples

**Example 1**

Input:

```python
median_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3)
```

Output:

```text
[1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
```

**Example 2**

Input:

```python
median_sliding_window([1, 2, 3, 4, 2, 3, 1, 4, 2], 3)
```

Output:

```text
[2.0, 3.0, 3.0, 3.0, 2.0, 3.0, 2.0]
```

### Constraints

- `1 <= k <= len(nums) <= 100000`
- `-10**9 <= nums[i] <= 10**9`

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

Keep the window's values **in sorted order** and read the middle. When the window slides, one value leaves and one enters. A **sorted list** with `bisect` does exactly that: `bisect.insort` inserts the new value, and `bisect_left` finds the old value to delete with `del`. List insertion and deletion shift elements, but that is a fast `memmove` in C, so it is quick in practice for the sizes here: `O(k)` per move with a tiny constant.

The textbook solution uses **two heaps with lazy deletion** (a heap cannot remove an arbitrary element, so you mark values as deleted and discard them only when they reach the top); it gives `O(n log k)`. The sorted list approach is shorter and just as good here.

## Explanation

`window` is always sorted. `insort` adds the entering value; `bisect_left` locates the leaving value (which is certainly in the list). The median is read by index.
