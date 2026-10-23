---
name: sheet-making-a-large-island
title: 'Making a Large Island'
tags: [dsa-sheet, graphs, disjoint-sets]
difficulty: Mastery
---

## Statement

`grid` holds `0` (water) and `1` (land). You may change **at most one `0` to `1`**. Return the **size of the largest island** (land cells connected up, down, left or right) you can get.

For `[[1, 0], [0, 1]]` the answer is `3`.

### Examples

**Example 1**

Input:

```python
largest_island([[1, 0], [0, 1]])
```

Output:

```text
3
```

**Example 2**

Input:

```python
largest_island([[1, 1], [1, 1]])
```

Output:

```text
4
```

### Constraints

- `0 <= rows, cols <= 300`
- Every cell is `0` or `1`.

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **grid** is a graph too: each cell is a node and its neighbours are the cells up, down, left and right (sometimes the diagonals as well).

Trying every water cell and flooding the grid each time costs `O((rows·cols)²)`. Instead, **label the islands once** with a flood fill: give each island an id and remember its size. Then for each water cell, look at its four neighbours, collect the **distinct island ids** around it (use a set so that one island next to the cell on two sides is counted once), and the island you would get by turning this cell into land has size `1 + sum of those islands' sizes`.

Take the maximum over all water cells (and over the existing islands, in case there is no water). If the grid is all land the answer is its whole size. `O(rows · cols)`.

## Explanation

`label[r][c]` is the island id of a land cell and `size[id]` its size. The set of neighbour ids makes sure a single island is added only once.
