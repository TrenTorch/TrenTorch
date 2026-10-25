---
name: sheet-unique-paths
title: 'Unique Paths'
tags: [dsa-sheet, dynamic-programming, grid-dp]
difficulty: Beginner
---

## Statement

A robot stands at the top-left cell of a `rows x cols` grid and moves only **right** or **down** to reach the bottom-right cell. Return the **number of different paths**. Return the answer modulo `10**9 + 7`.

For `rows = 3` and `cols = 7` the answer is `28`.

The starter code is a plain recursion. It is correct but too slow for big grids.

### Examples

**Example 1**

Input:

```python
unique_paths(3, 7)
```

Output:

```text
28
```

**Explanation:** The robot moves right 6 times and down 2 times. The number of unique paths is the number of ways to arrange these moves.

**Example 2**

Input:

```python
unique_paths(3, 2)
```

Output:

```text
3
```

**Explanation:** The robot moves right once and down twice. The number of unique paths is the number of ways to arrange these moves.

### Constraints

- `1 <= rows, cols <= 1000`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** `paths(r, c)`, the number of paths to cell `(r, c)`. **Transition:** the last move came from above or from the left: `paths(r, c) = paths(r - 1, c) + paths(r, c - 1)`. **Base cases:** the first row and the first column have exactly one path each.

One row of the table is enough: while moving along a row, `row[c]` (still holding the value from the row above) plus `row[c - 1]` (already updated) gives the new `row[c]`. `O(rows × cols)` time, `O(cols)` memory.

A closed formula exists too: every path has `rows - 1` downs and `cols - 1` rights in some order, so the answer is `C(rows + cols - 2, rows - 1)`.

## Explanation

`row[c] += row[c - 1]` combines the cell above (old `row[c]`) and the cell to the left.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                        | Variables                                   |
| -------------------------------------- | ------------------------------------------- |
| `mod = 10**9 + 7`                      | `mod = 1000000007`                          |
| `row[c] = (row[c] + row[c - 1]) % mod` | `row = [1, 2, 1, 1, 1, 1, 1], _ = 1, c = 1` |
| `row[c] = (row[c] + row[c - 1]) % mod` | `row = [1, 2, 3, 4, 1, 1, 1], c = 3`        |
| `row[c] = (row[c] + row[c - 1]) % mod` | `row = [1, 2, 3, 4, 5, 6, 1], c = 5`        |
| `for c in range(1, cols):`             | `row = [1, 2, 3, 4, 5, 6, 7], _ = 2, c = 1` |
| `for c in range(1, cols):`             | `row = [1, 3, 6, 4, 5, 6, 7], c = 3`        |
| `for c in range(1, cols):`             | `row = [1, 3, 6, 10, 15, 6, 7], c = 5`      |
| `return`                               | `returned = 28`                             |
