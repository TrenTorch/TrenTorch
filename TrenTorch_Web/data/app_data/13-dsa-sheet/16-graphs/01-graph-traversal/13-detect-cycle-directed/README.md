---
name: sheet-detect-cycle-directed
title: 'Cycle in a Directed Graph'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Advanced
---

## Statement

The graph has `n` nodes and **directed** `edges` `[a, b]` meaning an arrow from `a` to `b`. Return `True` if it contains a **directed cycle** (you can follow arrows and return to the start). A self-loop `[a, a]` is a cycle.

For `n = 3` and `edges = [[0, 1], [1, 2], [2, 0]]` the answer is `True`.

### Examples

**Example 1**

Input:

```python
has_cycle_directed(3, [[0, 1], [1, 2], [2, 0]])
```

Output:

```text
True
```

**Explanation:** The edges 0->1, 1->2, 2->0 create a closed loop, so a directed cycle exists and the function returns true.

**Example 2**

Input:

```python
has_cycle_directed(3, [[0, 1], [0, 2], [1, 2]])
```

Output:

```text
False
```

**Explanation:** All edges go from lower to higher indices (0->1, 0->2, 1->2) and no path returns to its start, so there is no directed cycle and the function returns false.

### Constraints

- `0 <= n <= 100000`
- `0 <= len(edges) <= 200000`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

For directed graphs, "visited" is not enough: meeting a visited node does not always mean a cycle (two arrows can lead to the same node). A cycle means you meet a node that is **still on the current path** (an ancestor in the DFS).

Use three states for each node: **unvisited**, **in progress** (on the current DFS path) and **done**. Reaching an in-progress node closes a cycle. A node becomes done once all its descendants are finished. Use an explicit stack to avoid deep recursion.

A second method is **Kahn's algorithm** (topological sort): repeatedly remove nodes with no incoming arrows; if some nodes can never be removed, they lie on or after a cycle. `O(n + m)`.

## Explanation

The iterative DFS keeps an index into each node's adjacency list so it can come back to a node after finishing a child. `state` is 0 (new), 1 (on the path) or 2 (done).

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                | Variables                                                       |
| ------------------------------ | --------------------------------------------------------------- |
| `adj = [[] for _ in range(n)]` | `adj = [[], [], []]`                                            |
| `for a, b in edges:`           | `adj = [[1], [], []], a = 1, b = 2`                             |
| `state = [0] * n`              | `adj = [[1], [2], [0]], a = 2, b = 0, state = [0, 0, 0]`        |
| `stack = [(start, 0)]`         | `state = [1, 0, 0], start = 0, stack = [(0, 0)]`                |
| `state[nxt] = 1`               | `state = [1, 1, 0], stack = [(0, 1)], node = 0, i = 0, nxt = 1` |
| `stack.append((node, i + 1))`  | `stack = [(0, 1), (1, 1)], node = 1`                            |
| `node, i = stack.pop()`        | `state = [1, 1, 1], node = 2, nxt = 2`                          |
| `return`                       | `returned = True`                                               |

### Complexity

- Time: O(n + m) where n is number of nodes and m edges.
- Extra space: O(n + m) for adjacency, state and stack.
- The brute force takes O(n^3) with n nodes.
