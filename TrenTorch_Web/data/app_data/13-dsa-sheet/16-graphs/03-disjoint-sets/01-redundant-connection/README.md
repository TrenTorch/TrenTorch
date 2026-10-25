---
name: sheet-redundant-connection
title: 'Redundant Connection'
tags: [dsa-sheet, graphs, disjoint-sets]
difficulty: Intermediate
---

## Statement

The nodes are numbered `1` to `n`. The `edges` list a tree with **one extra edge added**, so exactly one cycle exists. Return an edge that can be removed so that the rest is a tree. If several edges can be removed, return the one that appears **last** in `edges`.

For `[[1, 2], [1, 3], [2, 3]]` the answer is `[2, 3]`.

### Examples

**Example 1**

Input:

```python
find_redundant_connection([[1, 2], [1, 3], [2, 3]])
```

Output:

```text
[2, 3]
```

**Explanation:** The third edge connects nodes already in the same component, forming a cycle, so it is removed.

**Example 2**

Input:

```python
find_redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]])
```

Output:

```text
[1, 4]
```

**Explanation:** When the fourth edge is processed it connects nodes already connected, creating a cycle, and it is the last removable edge.

### Constraints

- `2 <= number of nodes <= 100000`
- `len(edges)` equals the number of nodes
- No other cycle exists apart from the one made by the extra edge.

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **disjoint set union (DSU)**, also called **union-find**, keeps track of a partition of items into groups. It supports two operations: `find(x)` returns the representative (the "leader") of the group of `x`, and `union(a, b)` merges the groups of `a` and `b`. Store a `parent` array where each item points toward its leader. Two tricks make it almost `O(1)` per operation: **path compression** (while walking up in `find`, point nodes closer to the root) and **union by size** (attach the smaller group under the larger). Two items are in the same group exactly when `find(a) == find(b)`.

Process the edges **in order**, adding each to the structure. An edge whose two ends are **already in the same group** closes a cycle: those two nodes were connected before, and this edge connects them a second time. In a graph with exactly one cycle, the first edge (in input order) that does this is the last edge of the cycle, which is the answer.

Each step is nearly `O(1)`, so the whole thing is `O(n α(n))` (practically linear).

## Explanation

`find` uses path halving. When `find(a) == find(b)` the edge is redundant; otherwise `union` merges the groups.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                        | Variables                                                             |
| -------------------------------------- | --------------------------------------------------------------------- |
| `parent = list(range(len(edges) + 2))` | `parent = [0, 1, 2, 3, 4]`                                            |
| `def find(a):`                         | `find = <function find_redundant_connection.<locals>.find at 0x00...` |
| `ra, rb = find(a), find(b)`            | `a = 1, b = 2, ra = 1, rb = 2`                                        |
| `parent[ra] = rb`                      | `parent = [0, 2, 2, 3, 4]`                                            |
| `ra, rb = find(a), find(b)`            | `b = 3, ra = 2, rb = 3`                                               |
| `parent[ra] = rb`                      | `parent = [0, 2, 3, 3, 4]`                                            |
| `ra, rb = find(a), find(b)`            | `a = 2, ra = 3`                                                       |
| `return`                               | `returned = [2, 3]`                                                   |

### Complexity

- Time: O(n) where n is number of edges.
- Extra space: O(n) extra for parent array.
- The brute force takes O(n^2) where n is number of edges.
