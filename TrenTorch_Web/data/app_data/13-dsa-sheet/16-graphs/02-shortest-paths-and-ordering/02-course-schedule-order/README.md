---
name: sheet-course-schedule-order
title: 'Course Order'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Advanced
---

## Statement

As in the previous question, a pair `[a, b]` means course `b` must be taken before course `a`. Return an **order in which all courses can be taken**. Many orders may exist; return the **lexicographically smallest** one (compare the first course, then the second, and so on). If it is impossible, return an empty list.

For `num_courses = 4` and `prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]` the answer is `[0, 1, 2, 3]`.

### Examples

**Example 1**

Input:

```python
find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
```

Output:

```text
[0, 1, 2, 3]
```

**Example 2**

Input:

```python
find_order(2, [[0, 1], [1, 0]])
```

Output:

```text
[]
```

### Constraints

- `0 <= num_courses <= 100000`
- `0 <= len(prerequisites) <= 200000`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **topological order** lists the nodes so that every arrow goes from an earlier to a later node. Kahn's algorithm builds one: repeatedly output a node with in-degree 0. To get the **smallest** order, always pick the smallest available node: keep the available nodes in a **min-heap** instead of a plain queue.

If the output has fewer than `n` nodes, the rest are in a cycle: return `[]`. With the heap the cost is `O((n + m) log n)`.

## Explanation

The heap holds the courses whose prerequisites are all taken. Popping the smallest gives the lexicographically smallest valid order.
