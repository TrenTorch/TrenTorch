---
name: sheet-dungeon-game
title: 'Dungeon Game'
tags: [dsa-sheet, dynamic-programming, grid-dp]
difficulty: Advanced
theory: filling-the-table-backwards-dungeon-game
---

## Statement

A knight starts at the top-left cell of a grid and must reach the bottom-right cell, moving **right or down**. Each cell changes his health by its value (negative: damage, positive: healing). His health must stay **at least 1** at all times (including after the last cell). Return the **smallest starting health** that makes the trip possible. An empty dungeon needs `1`.

For `[[-2, -3, 3], [-5, -10, 1], [10, 30, -5]]` the answer is `7`.

### Examples

**Example 1**

Input:

```python
calculate_minimum_hp([[-2, -3, 3], [-5, -10, 1], [10, 30, -5]])
```

Output:

```text
7
```

**Example 2**

Input:

```python
calculate_minimum_hp([[0]])
```

Output:

```text
1
```

### Constraints

- `0 <= rows, cols <= 500`
- `-1000 <= value <= 1000`

## Explanation

The table starts from the bottom-right and fills upwards and to the left; `inf` stands for cells outside the grid.

### Complexity

- Time: O(r * c). Every cell is computed once, walking backward from the exit.
- Space: O(c). One row of the table.
