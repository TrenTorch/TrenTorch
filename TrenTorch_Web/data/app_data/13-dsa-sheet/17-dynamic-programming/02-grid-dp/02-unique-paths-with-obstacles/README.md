---
name: sheet-unique-paths-with-obstacles
title: 'Unique Paths With Obstacles'
tags: [dsa-sheet, dynamic-programming, grid-dp]
difficulty: Intermediate
---

## Statement

`grid` has `0` (free) and `1` (blocked). A robot moves **right or down** from the top-left to the bottom-right cell, only through free cells. Return the **number of paths**. Return the answer modulo `10**9 + 7`.

For `[[0, 0, 0], [0, 1, 0], [0, 0, 0]]` the answer is `2`.

### Examples

**Example 1**

Input:

```python
unique_paths_obstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
```

Output:

```text
2
```

**Example 2**

Input:

```python
unique_paths_obstacles([[0, 1], [0, 0]])
```

Output:

```text
1
```

### Constraints

- `0 <= rows, cols <= 500`
- Every cell is `0` or `1`.

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

The same recurrence as unique paths, with one change: a **blocked cell has 0 paths** (it can never be stepped on). `paths(r, c) = 0` if blocked, else `paths(r - 1, c) + paths(r, c - 1)`. The start has 1 path unless it is blocked. Also if the end is blocked the answer is 0.

Keep one row: when you reach a blocked cell set `row[c] = 0`. `O(rows × cols)`.

## Explanation

A blocked cell resets its entry to zero, which also stops paths from flowing through it to later cells.
