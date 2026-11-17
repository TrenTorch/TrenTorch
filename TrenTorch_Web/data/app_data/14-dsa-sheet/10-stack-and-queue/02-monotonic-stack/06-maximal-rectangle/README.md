---
name: sheet-maximal-rectangle
title: 'Maximal Rectangle of Ones'
tags: [dsa-sheet, stack-and-queue, monotonic-stack]
difficulty: Mastery
theory: rectangles-inside-a-grid
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

## Explanation

`heights[j]` grows by one for each row with a `1` in column `j` and resets to `0` otherwise. `largest_in_histogram` is the stack solution of the previous question.

### Complexity

- Time: O(r * c). For every row the heights are updated in O(c) and the largest rectangle in the histogram is found in O(c).
- Space: O(c). The heights and the stack.
