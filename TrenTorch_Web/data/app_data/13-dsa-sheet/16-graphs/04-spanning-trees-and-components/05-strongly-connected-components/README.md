---
name: sheet-strongly-connected-components
title: 'Strongly Connected Components'
tags: [dsa-sheet, graphs, spanning-trees-and-components]
difficulty: Mastery
---

## Statement

In a **directed** graph with `n` nodes, two nodes are in the same **strongly connected component (SCC)** if each can reach the other. Return the number of SCCs.

For `n = 5` and `edges = [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]` the answer is `3` (`{0, 1, 2}`, `{3}`, `{4}`).

### Examples

**Example 1**

Input:

```python
count_scc(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]])
```

Output:

```text
3
```

**Explanation:** 0, 1 and 2 form a loop (0 to 1 to 2 to 0), so they can reach each other: one component. 3 and 4 can only be reached going forward (1 to 3 to 4), so each is a component by itself. That makes 3.

**Example 2**

Input:

```python
count_scc(3, [])
```

Output:

```text
3
```

**Explanation:** There are 3 nodes and no edges, so no node can reach another and each is a component by itself: 3.

### Constraints

- `0 <= n <= 100000`
- `0 <= len(edges) <= 200000`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

Components of an undirected graph are found by one search, but in a directed graph, reaching `b` from `a` does not mean `a` is reachable from `b`.

**Kosaraju's algorithm** uses two DFS passes:

1. Run a DFS on the graph and record the nodes in the order they **finish** (post-order).
2. Build the **reversed** graph (every arrow flipped). Process the nodes in **decreasing finish time**; each unvisited node starts a DFS on the reversed graph that visits exactly one SCC.

Why it works: the node that finishes last in pass 1 belongs to a "source" component; in the reversed graph you cannot leave that component into another unvisited one. `O(n + m)`; use explicit stacks for deep graphs.

## Explanation

`order` is the post-order of pass 1. The second loop counts how many times a new DFS on the reversed graph is needed.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                 | Variables                                                                                                                                                                                       |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `adj = [[] for _ in range(n)]`  | `adj = [[], [], [], [], []]`                                                                                                                                                                    |
| `rev[b].append(a)`              | `adj = [[1], [2, 3], [0], [], []], rev = [[2], [0], [1], [1], []], a = 1, b = 3`                                                                                                                |
| `seen[nxt] = True`              | `adj = [[1], [2, 3], [0], [4], []], rev = [[2], [0], [1], [1], [3]], a = 3, b = 4, seen = [True, True, False, False, False], order = [], start = 0, stack = [(0, 1)], node = 0, i = 0, nxt = 1` |
| `stack.append((node, i + 1))`   | `seen = [True, True, True, False, False], order = [2], stack = [(0, 1), (1, 2)], node = 1, i = 1, nxt = 0`                                                                                      |
| `node, i = stack.pop()`         | `seen = [True, True, True, True, True], order = [2, 4, 3], stack = [(0, 1)], i = 2, nxt = 4`                                                                                                    |
| `stack = [start]`               | `seen = [True, False, False, False, False], order = [2, 4, 3, 1, 0], stack = [0], node = 0, i = 1, count = 1`                                                                                   |
| `for start in reversed(order):` | `seen = [True, True, True, False, False], start = 3, stack = [], node = 1, nxt = 0`                                                                                                             |
| `return`                        | `returned = 3`                                                                                                                                                                                  |

### Complexity

- Time: O(n + m) where n is nodes and m is edges.
- Extra space: O(n + m) for adjacency lists and stacks.
- The brute force takes O(n^3) where n is nodes.
