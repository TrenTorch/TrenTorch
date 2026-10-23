---
name: sheet-number-of-islands
title: 'Number of Islands'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Beginner
---

## Statement

`grid` is a map of `1` (land) and `0` (water). An **island** is a group of land cells connected **up, down, left or right**. Return the **number of islands**.

For `[[1, 1, 0], [0, 1, 0], [0, 0, 1]]` the answer is `2`.

### Examples

**Example 1**

Input:

```python
num_islands([[1, 1, 0], [0, 1, 0], [0, 0, 1]])
```

Output:

```text
2
```

**Example 2**

Input:

```python
num_islands([[0, 0], [0, 0]])
```

Output:

```text
0
```

### Constraints

- `0 <= rows, cols <= 300`
- Every cell is `0` or `1`.

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **grid** is a graph too: each cell is a node and its neighbours are the cells up, down, left and right (sometimes the diagonals as well).

Scan the grid cell by cell. Every time you meet a **land cell that has not been visited**, you have found a new island: count it, then **flood it** with a BFS (or DFS) that marks every connected land cell as visited so that none of them is counted again. The number of floods started is the answer.

You can mark cells as visited by writing `0` into the grid (changing the input) or with a separate `visited` set. Use an explicit queue or stack: a recursive DFS on a 300 x 300 grid can go 90,000 calls deep and crash Python's recursion limit. `O(rows * cols)`.

## Explanation

Every cell is entered once. The outer loops look for unvisited land; `stack` is the flood fill of one island.
