---
name: sheet-minimum-falling-path-sum
title: 'Minimum Falling Path Sum'
tags: [dsa-sheet, dynamic-programming, grid-dp]
difficulty: Intermediate
---

## Statement

`matrix` is a grid of numbers. A **falling path** starts at any cell of the first row and moves down one row at a time, to the cell directly below or diagonally below left or right. Return the **smallest sum** of a falling path. An empty matrix gives `0`.

For `[[2, 1, 3], [6, 5, 4], [7, 8, 9]]` the answer is `13` (`1 + 5 + 7`).

### Examples

**Example 1**

Input:

```python
min_falling_path_sum([[2, 1, 3], [6, 5, 4], [7, 8, 9]])
```

Output:

```text
13
```

**Example 2**

Input:

```python
min_falling_path_sum([[-19, 57], [-40, -5]])
```

Output:

```text
-59
```

### Constraints

- `0 <= rows, cols <= 500`
- `-100 <= value <= 100`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** `best(r, c)`, the smallest sum of a falling path ending at `(r, c)`. **Transition:** arrive from the three cells above: `best(r, c) = matrix[r][c] + min(best(r - 1, c - 1), best(r - 1, c), best(r - 1, c + 1))` (ignoring cells outside the grid). **Base case:** the first row. **Answer:** the minimum of the last row.

Keep only the previous row. `O(rows × cols)`.

## Explanation

`prev` is the previous row of totals. The slice `prev[max(0, c - 1) : c + 2]` takes only the neighbours that exist.
