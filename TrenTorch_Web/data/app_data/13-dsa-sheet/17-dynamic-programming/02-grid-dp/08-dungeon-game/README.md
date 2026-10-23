---
name: sheet-dungeon-game
title: 'Dungeon Game'
tags: [dsa-sheet, dynamic-programming, grid-dp]
difficulty: Advanced
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

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

Forward DP fails: knowing the best health on arrival does not tell you the minimum you needed at the start (a path with more total healing may dip lower on the way). Reverse the question and work **backwards from the princess**.

**State:** `need(r, c)`, the smallest health required when **entering** cell `(r, c)`. **Transition:** after the cell the knight needs `min(need(r + 1, c), need(r, c + 1))` (the easier next step), so before it he needs that minus the cell's value, but never less than 1: `need(r, c) = max(1, min(next) - dungeon[r][c])`. **Base case:** past the last cell the requirement is `1`. **Answer:** `need(0, 0)`.

## Explanation

The table starts from the bottom-right and fills upwards and to the left; `inf` stands for cells outside the grid.
