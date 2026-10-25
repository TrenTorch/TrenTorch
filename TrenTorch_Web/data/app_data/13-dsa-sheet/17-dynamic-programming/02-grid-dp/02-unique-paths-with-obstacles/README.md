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

**Explanation:** The grid is 3x3 with one blocked center cell; right/down moves from start to end yield exactly 2 unobstructed paths.

**Example 2**

Input:

```python
unique_paths_obstacles([[0, 1], [0, 0]])
```

Output:

```text
1
```

**Explanation:** Grid is 2x2 with top-right cell blocked; only down-then-right path reaches bottom-right free cell.

### Constraints

- `0 <= rows, cols <= 500`
- Every cell is `0` or `1`.

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

The same recurrence as unique paths, with one change: a **blocked cell has 0 paths** (it can never be stepped on). `paths(r, c) = 0` if blocked, else `paths(r - 1, c) + paths(r, c - 1)`. The start has 1 path unless it is blocked. Also if the end is blocked the answer is 0.

Keep one row: when you reach a blocked cell set `row[c] = 0`. `O(rows × cols)`.

## Explanation

A blocked cell resets its entry to zero, which also stops paths from flowing through it to later cells.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                        | Variables                                     |
| -------------------------------------- | --------------------------------------------- |
| `rows = len(grid)`                     | `rows = 3`                                    |
| `row = [0] * cols`                     | `cols = 3, mod = 1000000007, row = [0, 0, 0]` |
| `for c in range(cols):`                | `row = [1, 0, 0], r = 0, c = 0`               |
| `for c in range(cols):`                | `row = [1, 1, 0], c = 2`                      |
| `for c in range(cols):`                | `row = [1, 1, 1], r = 1, c = 1`               |
| `for r in range(rows):`                | `row = [1, 0, 1], r = 2, c = 2`               |
| `row[c] = (row[c] + row[c - 1]) % mod` | `row = [1, 1, 1], c = 1`                      |
| `return`                               | `returned = 2`                                |

### Complexity

- Time: O(n * q) n is rows q is cols.
- Extra space: O(q) q is cols.
- The brute force takes O(2^(n+q)) n is rows q is cols.
