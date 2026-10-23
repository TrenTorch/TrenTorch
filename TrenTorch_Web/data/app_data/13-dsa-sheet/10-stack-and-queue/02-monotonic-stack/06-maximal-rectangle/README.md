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

**Example 2**

Input:

```python
maximal_rectangle([[0]])
```

Output:

```text
0
```

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
