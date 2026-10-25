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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                             | Variables                                                         |
| ----------------------------------------------------------- | ----------------------------------------------------------------- |
| `heap = [(matrix[r][0], r, 0) for r in range(len(matrix))]` | `heap = [(1, 0, 0), (10, 1, 0), (12, 2, 0)]`                      |
| `heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))`        | `heap = [(5, 0, 1), (12, 2, 0), (10, 1, 0)], _ = 1, r = 0, c = 0` |
| `heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))`        | `heap = [(9, 0, 2), (12, 2, 0), (10, 1, 0)], _ = 5, c = 1`        |
| `for _ in range(k - 1):`                                    | `heap = [(10, 1, 0), (12, 2, 0)], _ = 3, c = 2`                   |
| `for _ in range(k - 1):`                                    | `heap = [(11, 1, 1), (12, 2, 0)], _ = 4, r = 1, c = 0`            |
| `for _ in range(k - 1):`                                    | `heap = [(12, 2, 0), (13, 1, 2)], _ = 5, c = 1`                   |
| `heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))`        | `heap = [(13, 1, 2), (13, 2, 1)], _ = 12, r = 2, c = 0`           |
| `return`                                                    | `returned = 13`                                                   |

### Complexity

- Time: O(k log n), where n is the number of rows in the matrix.
- Extra space: O(n), where n is the number of rows in the matrix.
- The brute force takes O(n log n).
