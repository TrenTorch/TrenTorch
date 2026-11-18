---
name: sheet-swim-in-rising-water
title: 'Swim in Rising Water'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Advanced
theory: minimum-effort-paths
---

## Statement

`grid[r][c]` is the height of a platform. At time `t` the water level is `t`, and you can swim from a cell to a neighbour (up, down, left, right) if **both** have height at most `t`. You start at the top-left at time 0. Return the **least time** at which you can reach the bottom-right cell.

For `[[0, 2], [1, 3]]` the answer is `3`.

### Examples

**Example 1**

Input:

```python
swim_in_water([[0, 2], [1, 3]])
```

Output:

```text
3
```

**Example 2**

Input:

```python
swim_in_water([[0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16], [11, 17, 18, 19, 20], [10, 9, 8, 7, 6]])
```

Output:

```text
16
```

### Constraints

- `1 <= rows, cols <= 100`
- All heights are different integers from `0` to `rows * cols - 1`.

## Explanation

The heap starts with the top-left cell at time `grid[0][0]`. The first pop of the bottom-right cell gives the answer.

### Complexity

- Time: O(r * c * log(r * c)). Dijkstra-like search where the cost of a path is its highest cell; each cell is pushed once.
- Space: O(r * c). The visited grid and the heap.
