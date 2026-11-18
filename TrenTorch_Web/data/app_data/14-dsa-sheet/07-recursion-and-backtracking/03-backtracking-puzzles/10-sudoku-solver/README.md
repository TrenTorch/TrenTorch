---
name: sheet-sudoku-solver
title: 'Sudoku Solver'
tags: [dsa-sheet, recursion, backtracking-puzzles]
difficulty: Mastery
theory: sudoku
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

### Constraints

- The board is 9 by 9.
- Each puzzle has exactly one solution.

## Explanation

`rows`, `cols` and `boxes` hold the digits used so far. `go()` finds the empty cell with the fewest candidates; none means dead end (return `False`), otherwise it tries each candidate, placing it in the board and in the three sets, recursing, and undoing on failure. When no empty cell remains the puzzle is solved.

### Complexity

- Time: O(9^m) worst case, m = number of empty cells. Backtracking tries up to 9 digits per empty cell; always filling the cell with the fewest candidates prunes almost every branch on real puzzles, and Sudoku is NP-complete when generalised, so no polynomial method is known.
- Space: O(1). The board is a fixed 9 x 9 and the recursion is at most 81 deep.
