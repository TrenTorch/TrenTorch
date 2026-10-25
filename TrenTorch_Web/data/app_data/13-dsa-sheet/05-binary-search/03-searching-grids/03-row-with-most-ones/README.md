---
name: sheet-row-with-most-ones
title: 'Row With the Most Ones'
tags: [dsa-sheet, binary-search, searching-grids]
difficulty: Intermediate
---

## Statement

Every row of `matrix` contains only `0` and `1`, and each row is **sorted**: all its `0`s come before all its `1`s. Return the **index of the row with the most `1`s**. If several rows tie, return the smallest index. If there is no `1` anywhere, return `-1`.

### Examples

**Example 1**

Input:

```python
row_with_most_ones([[0, 0, 1, 1], [0, 1, 1, 1], [0, 0, 0, 1]])
```

Output:

```text
1
```

Row 1 has three `1`s.

**Example 2**

Input:

```python
row_with_most_ones([[0, 0], [0, 0]])
```

Output:

```text
-1
```

There is no `1`.

### Constraints

- `0 <= rows, cols`, and `rows * cols <= 2 * 10**5`
- Every row is sorted: zeros first, then ones.
- The big tests count how many cells you read.

## Theory

Counting the ones in every row means reading every cell: `O(rows * cols)`. Because each row is sorted, the number of ones in a row is `cols - (index of its first 1)`, and the index of the first `1` is a **lower bound** search: binary search for the first position where the value is `1`.

So the whole matrix costs `rows * log(cols)` reads instead of `rows * cols`. Keep the row with the most ones; comparing with a strict `>` keeps the smallest index when rows tie.

(There is an even faster `O(rows + cols)` staircase walk from the top-right corner, but the per-row binary search is the straightforward application of this topic.)

## Explanation

For each row, binary search the first index where the value is `1` (`hi = len(row)` if there is none). The count of ones is `len(row) - lo`. Update the best row only when the count is strictly greater, so ties keep the earlier row, and a matrix with no ones keeps `-1`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                    | Variables                                                                    |
| ---------------------------------- | ---------------------------------------------------------------------------- |
| `best_row, best = -1, 0`           | `best_row = -1, best = 0`                                                    |
| `hi = mid`                         | `i = 0, row = [0, 0, 1, 1], lo = 0, hi = 2, mid = 2`                         |
| `ones = len(row) - lo`             | `lo = 2, mid = 1, ones = 2`                                                  |
| `mid = (lo + hi) // 2`             | `best_row = 0, best = 2, i = 1, row = [0, 1, 1, 1], lo = 0, hi = 4, mid = 2` |
| `mid = (lo + hi) // 2`             | `hi = 1, mid = 0`                                                            |
| `for i, row in enumerate(matrix):` | `best_row = 1, best = 3, i = 2, row = [0, 0, 0, 1], lo = 1, ones = 3`        |
| `lo = mid + 1`                     | `lo = 3, hi = 4, mid = 2`                                                    |
| `return`                           | `returned = 1`                                                               |

### Complexity

- Time: O(n log m), n rows, m columns.
- Extra space: O(1), no extra structure.
- The brute force takes O(n*m), n rows, m columns.
