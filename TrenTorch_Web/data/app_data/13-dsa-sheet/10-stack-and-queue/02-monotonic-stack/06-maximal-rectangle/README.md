---
name: sheet-maximal-rectangle
title: 'Maximal Rectangle of Ones'
tags: [dsa-sheet, stack-and-queue, monotonic-stack]
difficulty: Mastery
---

## Statement

`matrix` is a grid of `0`s and `1`s. Return the **area of the largest rectangle made only of `1`s**.

For `[[1, 0, 1, 0, 0], [1, 0, 1, 1, 1], [1, 1, 1, 1, 1], [1, 0, 0, 1, 0]]` the answer is `6`.

### Examples

**Example 1**

Input:

```python
maximal_rectangle([[1, 0, 1, 0, 0], [1, 0, 1, 1, 1], [1, 1, 1, 1, 1], [1, 0, 0, 1, 0]])
```

Output:

```text
6
```

**Explanation:** Heights per column grow where row entries are 1, producing a histogram with a bar of height 2 spanning three consecutive columns. The largest rectangle in that histogram has area 6, and no row yields a larger all-1 rectangle.

**Example 2**

Input:

```python
maximal_rectangle([[0]])
```

Output:

```text
0
```

**Explanation:** The matrix contains a single zero cell, so heights are zero for the only column. The largest rectangle in the histogram has area 0, which is the maximum for an all-1 rectangle.

### Constraints

- `0 <= rows, cols <= 400`
- Every cell is `0` or `1`.

## Theory

A **stack** is last in, first out: you only add (`push`) and remove (`pop`) at the top. In Python a list does this with `append()` and `pop()`, both `O(1)`.

This reduces to the histogram question. Go row by row and keep, for each column, the **height of the stack of consecutive 1s ending at the current row** (a `0` resets the height to 0). Each row then looks like a histogram, and the largest rectangle that ends on this row's bottom edge is the largest rectangle in that histogram.

Take the best over all rows. Cost: `O(rows * cols)`: building the heights is `O(cols)` per row and the histogram algorithm is `O(cols)` per row.

This is a nice example of **reducing** a new problem to one you already solved.

## Explanation

`heights[j]` grows by one for each row with a `1` in column `j` and resets to `0` otherwise. `largest_in_histogram` is the stack solution of the previous question.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                | Variables                                                                                                                                                |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cols = len(matrix[0])`                        | `cols = 5`                                                                                                                                               |
| `for j in range(cols):`                        | `heights = [1, 0, 0, 0, 0], best = 0, largest_in_histogram = <function maximal_rectangle.<locals>.largest_in_histogram..., row = [1, 0, 1, 0, 0], j = 1` |
| `for row in matrix:`                           | `heights = [1, 0, 1, 0, 0], best = 1, row = [1, 0, 1, 1, 1], j = 4`                                                                                      |
| `heights[j] = heights[j] + 1 if row[j] else 0` | `heights = [2, 0, 2, 1, 0], j = 3`                                                                                                                       |
| `for j in range(cols):`                        | `heights = [3, 0, 2, 1, 1], best = 3, row = [1, 1, 1, 1, 1], j = 1`                                                                                      |
| `heights[j] = heights[j] + 1 if row[j] else 0` | `heights = [3, 1, 3, 2, 2], j = 4`                                                                                                                       |
| `heights[j] = heights[j] + 1 if row[j] else 0` | `heights = [4, 0, 3, 2, 2], best = 6, row = [1, 0, 0, 1, 0], j = 1`                                                                                      |
| `return`                                       | `returned = 6`                                                                                                                                           |

### Complexity

- Time: O(R*C) time where R is rows and C is columns.
- Extra space: O(C) extra memory where C is columns.
- The brute force takes O(R^3*C^3) time where R is rows and C is columns.
