---
name: sheet-most-stones-removed
title: 'Most Stones Removed'
tags: [dsa-sheet, graphs, disjoint-sets]
difficulty: Advanced
---

## Statement

Stones are placed on the integer grid, `stones[i] = [x, y]`, at most one per cell. You may **remove a stone** if there is another stone **in the same row or the same column** that has not been removed. Return the **largest number of stones** you can remove.

For `[[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]` the answer is `5`.

### Examples

**Example 1**

Input:

```python
remove_stones([[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]])
```

Output:

```text
5
```

**Example 2**

Input:

```python
remove_stones([[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]])
```

Output:

```text
3
```

### Constraints

- `0 <= len(stones) <= 100000`
- `0 <= x, y <= 10000`
- No two stones share a cell.

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **disjoint set union (DSU)**, also called **union-find**, keeps track of a partition of items into groups. It supports two operations: `find(x)` returns the representative (the "leader") of the group of `x`, and `union(a, b)` merges the groups of `a` and `b`. Store a `parent` array where each item points toward its leader. Two tricks make it almost `O(1)` per operation: **path compression** (while walking up in `find`, point nodes closer to the root) and **union by size** (attach the smaller group under the larger). Two items are in the same group exactly when `find(a) == find(b)`.

Call two stones **connected** if they share a row or a column. In each group of connected stones you can remove all stones **except one** (remove them in the order of a DFS from the last leaf backwards, so every removed stone still has a neighbour). Stones in different groups cannot help each other. The answer is `number of stones - number of groups`.

To count groups with union-find, you do not need to compare stones: treat each **row** and each **column** as an item, and union the row `x` with the column `y` for every stone (use `y + 10001` to keep the two kinds apart). Count the distinct leaders among the stones. `O(n α)`.

## Explanation

Every stone connects its row with its column; the groups of rows and columns are exactly the groups of connected stones.
