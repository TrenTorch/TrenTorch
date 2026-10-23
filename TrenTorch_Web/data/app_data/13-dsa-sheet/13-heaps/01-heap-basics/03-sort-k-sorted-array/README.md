---
name: sheet-sort-k-sorted-array
title: 'Sort a Nearly Sorted Array'
tags: [dsa-sheet, heaps, heap-basics]
difficulty: Intermediate
---

## Statement

Every value of `nums` is at most `k` positions away from the position it would have in the **sorted** list. Return the sorted list. Aim for `O(n log k)` time.

For `nums = [6, 5, 3, 2, 8, 10, 9]` and `k = 3` the answer is `[2, 3, 5, 6, 8, 9, 10]`.

### Examples

**Example 1**

Input:

```python
sort_k_sorted([6, 5, 3, 2, 8, 10, 9], 3)
```

Output:

```text
[2, 3, 5, 6, 8, 9, 10]
```

**Example 2**

Input:

```python
sort_k_sorted([3, 2, 1], 2)
```

Output:

```text
[1, 2, 3]
```

### Constraints

- `0 <= len(nums) <= 100000`
- `0 <= k <= len(nums)`
- `-10**9 <= nums[i] <= 10**9`

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

The smallest value of the whole list must be among the first `k + 1` values (it is at most `k` places from the front). So keep a **min-heap of `k + 1` values**. Pop the smallest: it is the next sorted value, and it is safe, because everything not yet in the heap is at least as large. Then push the next unread value and repeat.

The heap never holds more than `k + 1` items, so each step costs `O(log k)`: `O(n log k)` in total, better than a full sort when `k` is small. At the end pop the remaining values.

## Explanation

The first `k + 1` values go into the heap; afterwards every step pushes one value and pops one. The pops come out in sorted order.
