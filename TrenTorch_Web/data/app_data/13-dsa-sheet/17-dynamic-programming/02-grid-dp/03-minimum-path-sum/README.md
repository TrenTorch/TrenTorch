---
name: sheet-minimum-path-sum
title: 'Minimum Path Sum'
tags: [dsa-sheet, dynamic-programming, grid-dp]
difficulty: Beginner
---

## Statement

`grid` holds non-negative numbers. Move **right or down** from the top-left to the bottom-right cell. Return the **smallest possible sum** of the numbers on the path (both ends included). An empty grid gives `0`.

For `[[1, 3, 1], [1, 5, 1], [4, 2, 1]]` the answer is `7` (`1 + 3 + 1 + 1 + 1`).

The starter code is a plain recursion. It is correct but too slow for big grids.

### Examples

**Example 1**

Input:

```python
min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]])
```

Output:

```text
7
```

**Example 2**

Input:

```python
min_path_sum([[1, 2, 3], [4, 5, 6]])
```

Output:

```text
12
```

### Constraints

- `0 <= rows, cols <= 500`
- `0 <= grid[r][c] <= 100`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** `best(r, c)`, the smallest sum of a path ending at `(r, c)`. **Transition:** you arrive from above or from the left: `best(r, c) = grid[r][c] + min(best(r - 1, c), best(r, c - 1))`. **Base cases:** the first row and column have only one way in. One row of the table is enough. `O(rows × cols)`.

## Explanation

`row[c]` holds `best(r - 1, c)` before the update and the new `best(r, c)` after; `row[c - 1]` is the left neighbour.
