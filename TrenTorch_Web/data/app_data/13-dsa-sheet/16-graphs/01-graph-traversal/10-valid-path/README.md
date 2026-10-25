---
name: sheet-valid-path
title: 'Is There a Path?'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Beginner
---

## Statement

A graph has `n` nodes numbered `0` to `n - 1` and undirected `edges`. Return `True` if there is a **path from `source` to `destination`**.

For `n = 3`, `edges = [[0, 1], [1, 2], [2, 0]]`, `source = 0` and `destination = 2` the answer is `True`.

### Examples

**Example 1**

Input:

```python
valid_path(3, [[0, 1], [1, 2], [2, 0]], 0, 2)
```

Output:

```text
True
```

**Explanation:** The edges form a triangle connecting all nodes. Thus node 0 can reach node 2.

**Example 2**

Input:

```python
valid_path(6, [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]], 0, 5)
```

Output:

```text
False
```

**Explanation:** Edges link 0,1,2 together and 3,4,5 together. Source 0 and destination 5 are in separate components, so no path exists.

### Constraints

- `1 <= n <= 100000`
- `0 <= len(edges) <= 200000`
- `0 <= source, destination < n`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

Build the adjacency list, then run a BFS or DFS from `source`. If you reach `destination` the answer is `True`; if the search ends without it, `False`. A node is its own destination (`source == destination` is `True`). You can stop the search as soon as the destination is seen. `O(n + m)`.

## Explanation

The search marks nodes as seen so each is processed once, and stops early when the destination is found.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                | Variables                                                   |
| ------------------------------ | ----------------------------------------------------------- |
| `adj = [[] for _ in range(n)]` | `adj = [[], [], []]`                                        |
| `adj[b].append(a)`             | `adj = [[1], [0], []], a = 0, b = 1`                        |
| `adj[b].append(a)`             | `adj = [[1], [0, 2], [1]], a = 1, b = 2`                    |
| `adj[b].append(a)`             | `adj = [[1, 2], [0, 2], [1, 0]], a = 2, b = 0`              |
| `stack = [source]`             | `seen = [True, False, False], stack = [0]`                  |
| `seen[nxt] = True`             | `seen = [True, True, False], stack = [], node = 0, nxt = 1` |
| `seen[nxt] = True`             | `seen = [True, True, True], stack = [1], nxt = 2`           |
| `return`                       | `returned = True`                                           |

### Complexity

- Time: O(n + m).
- Extra space: O(n + m).
- The brute force takes O(n * m).
