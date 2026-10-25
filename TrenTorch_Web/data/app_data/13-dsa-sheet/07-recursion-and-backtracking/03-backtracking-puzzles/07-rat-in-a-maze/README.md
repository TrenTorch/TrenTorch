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

**Explanation:** From the start two valid non-repeating routes reach the goal: down down right down right right and down right down down right right; they appear in dictionary order.

**Example 2**

Input:

```python
rat_in_a_maze([[1, 0], [0, 1]])
```

Output:

```text
[]
```

**Explanation:** Start and goal are open but no adjacent open cells connect them; the only moves from start go to walls so no path exists.

### Constraints

- `0 <= rows, cols <= 6`
- Each cell is `0` or `1`.

## Theory

A depth-first search that **records the path** and **backtracks**: from the current cell try each of the four moves; if the next cell is inside the grid, open and not yet used on this path, step there and continue. When you reach the goal, save the path string. Then **unmark** the cell so other paths can use it.

Trying the moves in the order `D, L, R, U` (alphabetical) makes the paths come out already sorted.

The difference from a shortest-path search is that you want **all** paths, so you must undo the visited marks when you backtrack: a cell that was used by one path may be used by another.

## Explanation

`go(r, c)` returns immediately if the cell is closed or already on the current path. At the goal it records `"".join(path)`. Otherwise it marks the cell, tries `D, L, R, U` appending the letter to the path before each recursive call, and unmarks the cell on the way back.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                  | Variables                                                                                                                                |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `rows = len(maze)`                                               | `rows = 4`                                                                                                                               |
| `cols = len(maze[0]) if rows else 0`                             | `cols = 4`                                                                                                                               |
| `out = []`                                                       | `out = []`                                                                                                                               |
| `path = []`                                                      | `path = []`                                                                                                                              |
| `moves = (("D", 1, 0), ("L", 0, -1), ("R", 0, 1), ("U", -1, 0))` | `on_path = [[False, False, False, False], [False, False, False, Fals..., moves = (('D', 1, 0), ('L', 0, -1), ('R', 0, 1), ('U', -1, 0))` |
| `def go(r, c):`                                                  | `go = <function rat_in_a_maze.<locals>.go at 0x000001F4832C35B0>`                                                                        |
| `go(0, 0)`                                                       | `out = ['DDRDRR', 'DRDDRR']`                                                                                                             |
| `return`                                                         | `returned = ['DDRDRR', 'DRDDRR']`                                                                                                        |
