---
name: sheet-rat-in-a-maze
title: 'Rat in a Maze'
tags: [dsa-sheet, recursion, backtracking-puzzles]
difficulty: Intermediate
---

## Statement

`maze` is a grid of `0` (wall) and `1` (open). A rat starts at the **top-left** cell and must reach the **bottom-right** cell, moving **up, down, left or right** through open cells, never visiting a cell twice in the same path.

Return **every such path** as a string of moves `D` (down), `L` (left), `R` (right), `U` (up), sorted in dictionary order. If the start or the goal is a wall, or no path exists, return `[]`. If the grid is a single open cell, the one path is the empty string: `[""]`.

### Examples

**Example 1**

Input:

```python
rat_in_a_maze([[1, 0, 0, 0], [1, 1, 0, 1], [1, 1, 0, 0], [0, 1, 1, 1]])
```

Output:

```text
['DDRDRR', 'DRDDRR']
```

**Example 2**

Input:

```python
rat_in_a_maze([[1, 0], [0, 1]])
```

Output:

```text
[]
```

### Constraints

- `0 <= rows, cols <= 6`
- Each cell is `0` or `1`.

## Theory

A depth-first search that **records the path** and **backtracks**: from the current cell try each of the four moves; if the next cell is inside the grid, open and not yet used on this path, step there and continue. When you reach the goal, save the path string. Then **unmark** the cell so other paths can use it.

Trying the moves in the order `D, L, R, U` (alphabetical) makes the paths come out already sorted.

The difference from a shortest-path search is that you want **all** paths, so you must undo the visited marks when you backtrack: a cell that was used by one path may be used by another.

## Explanation

`go(r, c)` returns immediately if the cell is closed or already on the current path. At the goal it records `"".join(path)`. Otherwise it marks the cell, tries `D, L, R, U` appending the letter to the path before each recursive call, and unmarks the cell on the way back.
