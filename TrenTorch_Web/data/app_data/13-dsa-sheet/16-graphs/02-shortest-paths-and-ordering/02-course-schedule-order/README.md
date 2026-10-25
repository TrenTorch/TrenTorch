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

**Explanation:** Course 0 has no prerequisites, so it is taken first; then courses 1 and 2 become available, and the smallest (1) is taken before 2, after which 3's prerequisites are satisfied.

**Example 2**

Input:

```python
find_order(2, [[0, 1], [1, 0]])
```

Output:

```text
[]
```

**Explanation:** The two courses depend on each other, forming a cycle, so no ordering can satisfy all prerequisites, resulting in an empty list.

### Constraints

- `0 <= num_courses <= 100000`
- `0 <= len(prerequisites) <= 200000`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **topological order** lists the nodes so that every arrow goes from an earlier to a later node. Kahn's algorithm builds one: repeatedly output a node with in-degree 0. To get the **smallest** order, always pick the smallest available node: keep the available nodes in a **min-heap** instead of a plain queue.

If the output has fewer than `n` nodes, the rest are in a cycle: return `[]`. With the heap the cost is `O((n + m) log n)`.

## Explanation

The heap holds the courses whose prerequisites are all taken. Popping the smallest gives the lexicographically smallest valid order.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                          | Variables                                                                                 |
| ---------------------------------------- | ----------------------------------------------------------------------------------------- |
| `adj = [[] for _ in range(num_courses)]` | `adj = [[], [], [], []]`                                                                  |
| `for course, pre in prerequisites:`      | `adj = [[1], [], [], []], in_degree = [0, 1, 0, 0], course = 2, pre = 0`                  |
| `in_degree[course] += 1`                 | `adj = [[1, 2], [3], [], []], in_degree = [0, 1, 1, 1], course = 3, pre = 1`              |
| `order = []`                             | `adj = [[1, 2], [3], [3], []], in_degree = [0, 1, 1, 2], pre = 2, heap = [0], order = []` |
| `in_degree[nxt] -= 1`                    | `in_degree = [0, 0, 1, 2], heap = [], order = [0], node = 0, nxt = 1`                     |
| `node = heapq.heappop(heap)`             | `in_degree = [0, 0, 0, 2], heap = [2], node = 1, nxt = 2`                                 |
| `order.append(node)`                     | `in_degree = [0, 0, 0, 1], heap = [], order = [0, 1, 2], node = 2, nxt = 3`               |
| `return`                                 | `returned = [0, 1, 2, 3]`                                                                 |
