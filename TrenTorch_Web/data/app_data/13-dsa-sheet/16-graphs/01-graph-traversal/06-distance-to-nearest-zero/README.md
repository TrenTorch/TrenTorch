---
name: sheet-distance-to-nearest-zero
title: 'Distance to the Nearest Zero'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Intermediate
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

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **grid** is a graph too: each cell is a node and its neighbours are the cells up, down, left and right (sometimes the diagonals as well).

Asking "how far is the nearest zero" for every cell separately is expensive. Turn the question around: **start from all the zeros at once** and spread outwards, one step per BFS level (a **multi-source BFS**, as in rotting oranges). A cell is reached for the first time from its nearest zero, so that BFS level is its distance.

Initialise the answer with `0` at zeros and "unknown" elsewhere; push every zero into the queue; when you pop a cell, give each unknown neighbour `distance + 1` and queue it. `O(rows * cols)`.

## Explanation

`dist` starts at -1 (unknown) for the ones. The queue begins with all the zeros, so BFS levels equal distances.
