---
name: sheet-kth-smallest-in-sorted-matrix
title: 'Kth Smallest in a Sorted Matrix'
tags: [dsa-sheet, heaps, heap-basics]
difficulty: Intermediate
---

## Statement

`matrix` has every **row sorted** and every **column sorted** in increasing order. Return the **`k`-th smallest** value (counting from 1, repeated values counted separately).

For `[[1, 5, 9], [10, 11, 13], [12, 13, 15]]` and `k = 8` the answer is `13`.

### Examples

**Example 1**

Input:

```python
kth_smallest_matrix([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8)
```

Output:

```text
13
```

**Example 2**

Input:

```python
kth_smallest_matrix([[-5]], 1)
```

Output:

```text
-5
```

### Constraints

- `1 <= rows, cols <= 300`
- `1 <= k <= rows * cols`
- `-10**9 <= value <= 10**9`

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

The smallest value is the top-left cell. After removing a cell, the next candidate is the cell **below** it or the cell **to its right**. Use a min-heap of candidate cells `(value, row, col)`. Start with the first cell of every row (or just cell `(0, 0)`); pop `k - 1` times, and each time push the neighbours of the popped cell: the one to its right in the same row. The `k`-th pop is the answer.

Starting with the first cell of each row and only pushing the cell to the right needs no visited set. The cost is `O((rows + k) log rows)`, far better than sorting all `rows * cols` values when `k` is small.

## Explanation

The heap has at most one candidate per row. Popping the smallest candidate `k` times yields the values in sorted order.
