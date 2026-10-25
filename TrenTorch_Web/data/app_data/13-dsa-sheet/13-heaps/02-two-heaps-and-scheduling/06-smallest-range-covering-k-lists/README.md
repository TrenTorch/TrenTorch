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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                          | Variables                                                                                           |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `heap = [(lst[0], i, 0) for i, lst in enumerate(lists)]` | `heap = [(4, 0, 0), (0, 1, 0), (5, 2, 0)]`                                                          |
| `nxt = lists[i][j + 1]`                                  | `heap = [(4, 0, 0), (5, 2, 0)], current_max = 5, best = [0, 5], value = 0, i = 1, j = 0, nxt = 9`   |
| `current_max = max(current_max, nxt)`                    | `heap = [(5, 2, 0), (9, 1, 1)], current_max = 10, value = 4, i = 0, nxt = 10`                       |
| `heapq.heappush(heap, (nxt, i, j + 1))`                  | `heap = [(9, 1, 1), (10, 0, 1), (18, 2, 1)], current_max = 18, value = 5, i = 2, nxt = 18`          |
| `nxt = lists[i][j + 1]`                                  | `heap = [(12, 1, 2), (18, 2, 1)], value = 10, i = 0, j = 1, nxt = 15`                               |
| `heapq.heappush(heap, (nxt, i, j + 1))`                  | `heap = [(15, 0, 2), (18, 2, 1), (20, 1, 3)], current_max = 20, value = 12, i = 1, j = 2, nxt = 20` |
| `value, i, j = heapq.heappop(heap)`                      | `heap = [(20, 1, 3), (24, 0, 3)], current_max = 24, value = 18, i = 2, j = 1, nxt = 24`             |
| `return`                                                 | `returned = [20, 24]`                                                                               |

### Complexity

- Time: O(N log k) where N is total elements and k is lists.
- Extra space: O(k) for the heap.
- The brute force takes O(N^2) where N is total elements.
