---
name: sheet-sudoku-solver
title: 'Sudoku Solver'
tags: [dsa-sheet, recursion, backtracking-puzzles]
difficulty: Mastery
---

## Statement

`board` is a 9 by 9 Sudoku puzzle: digits `1` to `9` for given cells and `0` for empty cells. Return the **completed board**, where every row, every column and every `3 x 3` box contains each digit from `1` to `9` exactly once, and the given digits are unchanged. Every puzzle in the tests has exactly one solution.

### Examples

**Example 1**

Input:

```python
sudoku_solver([[5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0], [0, 9, 8, 0, 0, 0, 0, 6, 0], [8, 0, 0, 0, 6, 0, 0, 0, 3], [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6], [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 7, 9]])
```

Output:

```text
[[5, 3, 4, 6, 7, 8, 9, 1, 2], [6, 7, 2, 1, 9, 5, 3, 4, 8], [1, 9, 8, 3, 4, 2, 5, 6, 7], [8, 5, 9, 7, 6, 1, 4, 2, 3], [4, 2, 6, 8, 5, 3, 7, 9, 1], [7, 1, 3, 9, 2, 4, 8, 5, 6], [9, 6, 1, 5, 3, 7, 2, 8, 4], [2, 8, 7, 4, 1, 9, 6, 3, 5], [3, 4, 5, 2, 8, 6, 1, 7, 9]]
```

**Explanation:** The solver places digits that satisfy row, column, and box constraints, producing the unique solution, matching the output.

### Constraints

- The board is 9 by 9.
- Each puzzle has exactly one solution.

## Theory

Sudoku is **backtracking** on a grid. Pick an empty cell, try the digits `1` to `9` that do not clash with its row, column or box, place one, and recurse; if the rest of the puzzle cannot be completed, remove it and try the next digit.

Plain left-to-right filling can take a very long time on hard puzzles. The big improvement is to always fill the cell with the **fewest possible digits** ("most constrained first"): a cell with one candidate is forced, and a cell with none means you must backtrack right away. Keep sets of the digits already used in each row, column and box so candidates are found in `O(1)`.

This one search idea, "choose the most constrained choice first", is what makes many hard puzzle solvers practical.

## Explanation

`rows`, `cols` and `boxes` hold the digits used so far. `go()` finds the empty cell with the fewest candidates; none means dead end (return `False`), otherwise it tries each candidate, placing it in the board and in the three sets, recursing, and undoing on failure. When no empty cell remains the puzzle is solved.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                       | Variables                                                                                                                                                                                                                                                                                                  |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `grid = [list(row) for row in board]` | `grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0]...`                                                                                                                                                                                                                                      |
| `empty.append((r, c))`                | `rows = [{3, 5, 7}, set(), set(), set(), set(), set(), set(), set..., cols = [{5}, {3}, set(), set(), {7}, set(), set(), set(), set()], boxes = [{3, 5}, {7}, set(), set(), set(), set(), set(), set(), s..., empty = [(0, 2), (0, 3), (0, 5), (0, 6)], r = 0, c = 6, v = 0`                               |
| `boxes[r // 3 * 3 + c // 3].add(v)`   | `rows = [{3, 5, 7}, {1, 5, 6, 9}, set(), set(), set(), set(), set..., cols = [{5, 6}, {3}, set(), {1}, {9, 7}, {5}, set(), set(), set()], boxes = [{3, 5, 6}, {1, 5, 9, 7}, set(), set(), set(), set(), set..., empty = [(0, 2), (0, 3), (0, 5), (0, 6), (0, 7), (0, 8), (1, 1), ..., r = 1, c = 5, v = 5` |
| `for c in range(9):`                  | `rows = [{3, 5, 7}, {1, 5, 6, 9}, {8, 9, 6}, set(), set(), set(),..., cols = [{5, 6}, {9, 3}, {8}, {1}, {9, 7}, {5}, set(), {6}, set()], boxes = [{3, 5, 6, 8, 9}, {1, 5, 9, 7}, {6}, set(), set(), set(),..., r = 3, c = 0, v = 0`                                                                        |
| `for c in range(9):`                  | `rows = [{3, 5, 7}, {1, 5, 6, 9}, {8, 9, 6}, {8, 3, 6}, {4}, set(..., cols = [{8, 4, 5, 6}, {9, 3}, {8}, {1}, {9, 6, 7}, {5}, set(), {..., boxes = [{3, 5, 6, 8, 9}, {1, 5, 9, 7}, {6}, {8, 4}, {6}, {3}, se..., r = 4, c = 2`                                                                             |
| `cols[c].add(v)`                      | `rows = [{3, 5, 7}, {1, 5, 6, 9}, {8, 9, 6}, {8, 3, 6}, {8, 1, 3,..., cols = [{4, 5, 6, 7, 8}, {9, 3}, {8}, {8, 1}, {9, 2, 6, 7}, {3, ..., boxes = [{3, 5, 6, 8, 9}, {1, 5, 9, 7}, {6}, {8, 4, 7}, {8, 3, 6}..., r = 5, c = 4, v = 2`                                                                      |
| `v = grid[r][c]`                      | `cols = [{4, 5, 6, 7, 8}, {9, 3, 6}, {8}, {8, 1}, {9, 2, 6, 7}, {..., boxes = [{3, 5, 6, 8, 9}, {1, 5, 9, 7}, {6}, {8, 4, 7}, {8, 2, 3,..., r = 7, c = 3, v = 4`                                                                                                                                           |
| `return`                              | `returned = [[5, 3, 4, 6, 7, 8, 9, 1, 2], [6, 7, 2, 1, 9, 5, 3, 4, 8]...`                                                                                                                                                                                                                                  |
