---
name: sheet-course-schedule
title: 'Course Schedule'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Intermediate
---

## Statement

There are `num_courses` courses numbered `0` to `num_courses - 1`. A pair `[a, b]` in `prerequisites` means you must take course `b` **before** course `a`. Return `True` if it is possible to take **all** the courses.

For `num_courses = 2` and `prerequisites = [[1, 0]]` the answer is `True`; with `[[1, 0], [0, 1]]` it is `False`.

### Examples

**Example 1**

Input:

```python
can_finish(2, [[1, 0]])
```

Output:

```text
True
```

**Explanation:** With prerequisite [1,0], course 0 has no prerequisites, so take it first then 1, no cycle, True.

**Example 2**

Input:

```python
can_finish(2, [[1, 0], [0, 1]])
```

Output:

```text
False
```

**Explanation:** Prerequisites create cycle 1->0 and 0->1, impossible to order, False.

### Constraints

- `0 <= num_courses <= 100000`
- `0 <= len(prerequisites) <= 200000`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

Draw an arrow `b -> a` for each prerequisite pair. All courses can be taken exactly when this directed graph has **no cycle** (a cycle means a course is a prerequisite of itself). Finding an order is a **topological sort**.

**Kahn's algorithm**: count the **in-degree** of each node (its number of prerequisites). Put the nodes with in-degree 0 in a queue; they can be taken first. When you take a course, decrease the in-degree of the courses that need it; when one reaches 0, queue it. If you manage to take all `n` courses there is no cycle; if some are never queued, they are stuck in a cycle. `O(n + m)`.

## Explanation

`taken` counts the courses removed from the queue. It equals `num_courses` exactly when the graph has no cycle.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                          | Variables                                 |
| ---------------------------------------- | ----------------------------------------- |
| `adj = [[] for _ in range(num_courses)]` | `adj = [[], []]`                          |
| `for course, pre in prerequisites:`      | `in_degree = [0, 0], course = 1, pre = 0` |
| `in_degree[course] += 1`                 | `adj = [[1], []], in_degree = [0, 1]`     |
| `taken = 0`                              | `queue = deque([0]), taken = 0`           |
| `taken += 1`                             | `queue = deque([]), taken = 1, node = 0`  |
| `in_degree[nxt] -= 1`                    | `in_degree = [0, 0], nxt = 1`             |
| `node = queue.popleft()`                 | `node = 1`                                |
| `return`                                 | `returned = True`                         |
