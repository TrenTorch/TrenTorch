---
name: sheet-pacific-atlantic-water-flow
title: 'Pacific Atlantic Water Flow'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Advanced
theory: dfs-from-the-borders
---

## Statement

`heights[r][c]` is the height of a cell. Water flows from a cell to a neighbour (up, down, left, right) that is **at the same height or lower**. The **Pacific** ocean touches the top and left edges, the **Atlantic** touches the bottom and right edges. Return, as `[row, col]` pairs sorted by row and then column, **all cells from which water can reach both oceans**.

For `[[1, 2], [2, 1]]` the answer is `[[0, 1], [1, 0]]`.

### Examples

**Example 1**

Input:

```python
pacific_atlantic([[1, 2], [2, 1]])
```

Output:

```text
[[0, 1], [1, 0]]
```

**Example 2**

Input:

```python
pacific_atlantic([[1]])
```

Output:

```text
[[0, 0]]
```

### Constraints

- `0 <= rows, cols <= 200`
- `0 <= heights[r][c] <= 10**5`

## Explanation

`flood(starts)` returns the set of cells that water can reach by moving to equal or higher neighbours, starting from the cells next to one ocean. The answer is the cells that are in both sets, listed in row order by scanning the grid once, so no sort is needed.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                                  | Variables                                                              |
| -------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `rows = len(heights)`                                                            | `rows = 2`                                                             |
| `cols = len(heights[0]) if rows else 0`                                          | `cols = 2`                                                             |
| `def flood(starts):`                                                             | `flood = <function pacific_atlantic.<locals>.flood at 0x000002BDE7...` |
| `pacific = flood([(r, 0) for r in range(rows)] + [(0, c) for c in range(cols)])` | `pacific = {(1, 0), (0, 1), (0, 0)}`                                   |
| `atlantic = flood(`                                                              | `atlantic = {(0, 1), (1, 0), (1, 1)}`                                  |
| `return`                                                                         | `returned = [[0, 1], [1, 0]]`                                          |

### Complexity

- Time: O(r * c). Two searches walk uphill from the two coasts, each cell is visited at most once per search, and the answer is collected in row order.
- Space: O(r * c). The two visited sets and the stack.
