---
name: sheet-path-with-minimum-effort
title: 'Path With Minimum Effort'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Advanced
theory: minimum-effort-paths
---

## Statement

`heights[r][c]` is the height of a cell. You walk from the top-left to the bottom-right cell, moving up, down, left or right. The **effort** of a path is the **largest absolute difference in height between two neighbouring cells on the path**. Return the **smallest effort** over all paths.

For `[[1, 2, 2], [3, 8, 2], [5, 3, 5]]` the answer is `2`.

### Examples

**Example 1**

Input:

```python
minimum_effort_path([[1, 2, 2], [3, 8, 2], [5, 3, 5]])
```

Output:

```text
2
```

**Example 2**

Input:

```python
minimum_effort_path([[1, 2, 3], [3, 8, 4], [5, 3, 5]])
```

Output:

```text
1
```

### Constraints

- `1 <= rows, cols <= 100`
- `1 <= heights[r][c] <= 10**6`

## Explanation

`effort[r][c]` is the best known maximum difference to reach the cell. The heap pops cells in order of effort, and `max(...)` combines the path so far with the new step.

### Complexity

- Time: O(r * c * log(r * c)). Dijkstra where the cost of a path is its largest step; each cell can push a few heap entries.
- Space: O(r * c). The effort grid and the heap.
