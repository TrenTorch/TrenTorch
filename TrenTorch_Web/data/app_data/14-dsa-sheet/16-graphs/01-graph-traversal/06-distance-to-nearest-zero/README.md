---
name: sheet-distance-to-nearest-zero
title: 'Distance to the Nearest Zero'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Intermediate
theory: many-starting-points-at-once
---

## Statement

`mat` contains `0`s and `1`s, with **at least one `0`** (when it is not empty). For every cell return the **distance to the nearest `0`**, where a step moves up, down, left or right. A `0` cell has distance `0`.

For `[[0, 0, 0], [0, 1, 0], [1, 1, 1]]` the answer is `[[0, 0, 0], [0, 1, 0], [1, 2, 1]]`.

The starter code compares every cell with every zero. It is correct but too slow for a large grid.

### Examples

**Example 1**

Input:

```python
nearest_zero([[0, 0, 0], [0, 1, 0], [1, 1, 1]])
```

Output:

```text
[[0, 0, 0], [0, 1, 0], [1, 2, 1]]
```

**Example 2**

Input:

```python
nearest_zero([[0, 1]])
```

Output:

```text
[[0, 1]]
```

### Constraints

- `0 <= rows, cols <= 200`
- Every cell is `0` or `1`, and there is at least one `0`.

## Explanation

`dist` starts at -1 (unknown) for the ones. The queue begins with all the zeros, so BFS levels equal distances.

### Complexity

- Time: O(r * c). A breadth-first search started from every zero at once; each cell is set once.
- Space: O(r * c). The distance grid (the result) and the queue.
