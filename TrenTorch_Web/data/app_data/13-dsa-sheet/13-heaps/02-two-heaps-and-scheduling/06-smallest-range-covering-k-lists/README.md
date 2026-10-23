---
name: sheet-smallest-range-covering-k-lists
title: 'Smallest Range Covering K Lists'
tags: [dsa-sheet, heaps, two-heaps-and-scheduling]
difficulty: Mastery
---

## Statement

`lists` holds `k` lists of numbers, each sorted in increasing order and non-empty. Find the **smallest range `[lo, hi]`** that contains **at least one number from every list**. A range `[a, b]` is smaller than `[c, d]` if `b - a < d - c`, or if the lengths are equal and `a < c`. Return `[lo, hi]`.

For `[[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]` the answer is `[20, 24]`.

### Examples

**Example 1**

Input:

```python
smallest_range([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]])
```

Output:

```text
[20, 24]
```

**Example 2**

Input:

```python
smallest_range([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
```

Output:

```text
[1, 1]
```

### Constraints

- `1 <= k <= 3500`
- `1 <= total number of values <= 100000`
- `-10**5 <= value <= 10**5`

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

A range that covers every list always has one chosen number from each list. Its low end is the **minimum** of the chosen numbers and its high end is the **maximum**. Start with the **first number of each list**; their min and max form a valid range. To improve it, the only useful move is to replace the **minimum** (making the low end larger): take the next number of the list that holds the minimum.

A **min-heap** holds the current choice from each list, so the minimum is the top. Keep the current maximum in a variable. Repeat: record `[top, max]` if it is smaller than the best; pop the top, push the next number from the same list (updating the maximum). Stop when a list runs out of numbers.

`O(N log k)`.

## Explanation

The heap stores `(value, list_index, position)`. `current_max` is the largest value currently chosen. When any list is exhausted, no range can cover all lists any more.
