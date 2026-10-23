---
name: sheet-minimum-height-trees
title: 'Minimum Height Trees'
tags: [dsa-sheet, graphs, spanning-trees-and-components]
difficulty: Advanced
---

## Statement

The `edges` form a **tree** on the nodes `0` to `n - 1`. Any node can be chosen as the root, giving a rooted tree with some **height** (the number of edges on the longest path down from the root). Return all the roots that give the **smallest height**, in increasing order.

For `n = 6` and `edges = [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]` the answer is `[3, 4]`.

The starter code measures the height from every possible root. It is correct but too slow for a big tree.

### Examples

**Example 1**

Input:

```python
min_height_trees(6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]])
```

Output:

```text
[3, 4]
```

**Example 2**

Input:

```python
min_height_trees(4, [[1, 0], [1, 2], [1, 3]])
```

Output:

```text
[1]
```

### Constraints

- `1 <= n <= 100000`
- `len(edges) == n - 1` and the edges form a tree.

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

The best roots are at the **centre** of the tree. A tree has either one centre or two, and you find it by **peeling leaves**: remove all the leaves (nodes of degree 1), then the new leaves, and so on, layer by layer, like peeling an onion. When at most two nodes remain, they are the centres, and these are the roots of minimum height.

Implement it like Kahn's algorithm: keep degrees, start a queue with the leaves, and process level by level, reducing the number of remaining nodes until 2 or fewer are left. `O(n)`. For `n <= 2` all nodes are answers.

## Explanation

`remaining` is the number of nodes still in the tree; every round removes the current leaves and exposes new ones.
