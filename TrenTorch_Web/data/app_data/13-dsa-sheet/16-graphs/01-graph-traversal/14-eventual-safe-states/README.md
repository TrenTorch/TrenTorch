---
name: sheet-eventual-safe-states
title: 'Eventual Safe Nodes'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Advanced
---

## Statement

The directed graph has `n` nodes and `edges` `[a, b]` (arrows from `a` to `b`). A node with no outgoing arrows is **terminal**. A node is **safe** if **every** path starting at it eventually reaches a terminal node (it cannot be trapped in a cycle). Return the safe nodes in increasing order.

For `n = 7` and `edges = [[0, 1], [0, 2], [1, 2], [1, 3], [2, 5], [3, 0], [4, 5]]` the answer is `[2, 4, 5, 6]`.

### Examples

**Example 1**

Input:

```python
eventual_safe_nodes(7, [[0, 1], [0, 2], [1, 2], [1, 3], [2, 5], [3, 0], [4, 5]])
```

Output:

```text
[2, 4, 5, 6]
```

**Explanation:** Nodes 2,4,5,6 are safe because every path from them reaches a terminal node or ends. The cycle 0->1->3->0 traps only these and no others.

**Example 2**

Input:

```python
eventual_safe_nodes(5, [[1, 2], [2, 3], [3, 4], [4, 1]])
```

Output:

```text
[0]
```

**Explanation:** Only node 0 is safe. Nodes 1,2,3,4 form a cycle and can never reach a terminal, so they are unsafe.

### Constraints

- `0 <= n <= 100000`
- `0 <= len(edges) <= 200000`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A node is **unsafe** if it lies on a cycle or can reach one. Safe nodes are those that cannot. Work backwards from the terminal nodes: a node whose outgoing arrows **all** lead to safe nodes is itself safe.

This is Kahn's algorithm on the **reversed graph**: for every node count its outgoing arrows (`out_degree`). Start with the terminal nodes (out-degree 0) in a queue. When you pop a node, for each node `p` that has an arrow **to** it, decrease `out_degree[p]`; when it reaches 0, all of `p`'s arrows lead to safe nodes, so `p` is safe: queue it. The safe nodes are the ones that get processed. `O(n + m)`.

## Explanation

`rev[v]` lists the nodes with an arrow into `v`. The queue starts with the terminal nodes and grows with nodes whose outgoing arrows are all accounted for.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                | Variables                                                                                                                                                                                 |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rev = [[] for _ in range(n)]` | `rev = [[], [], [], [], [], [], []]`                                                                                                                                                      |
| `rev[b].append(a)`             | `rev = [[], [0], [0], [], [], [], []], out_degree = [1, 0, 0, 0, 0, 0, 0], a = 0, b = 2`                                                                                                  |
| `rev[b].append(a)`             | `rev = [[], [0], [0, 1], [1], [], [], []], out_degree = [2, 1, 0, 0, 0, 0, 0], a = 1, b = 3`                                                                                              |
| `rev[b].append(a)`             | `rev = [[3], [0], [0, 1], [1], [], [2], []], out_degree = [2, 2, 1, 0, 0, 0, 0], a = 3, b = 0`                                                                                            |
| `node = queue.popleft()`       | `rev = [[3], [0], [0, 1], [1], [], [2, 4], []], out_degree = [2, 2, 1, 1, 1, 0, 0], a = 4, b = 5, queue = deque([6]), safe = [False, False, False, False, False, False, False], node = 5` |
| `out_degree[p] -= 1`           | `out_degree = [2, 2, 0, 1, 0, 0, 0], queue = deque([6, 2]), safe = [False, False, False, False, False, True, False], p = 4`                                                               |
| `for p in rev[node]:`          | `queue = deque([4]), safe = [False, False, True, False, False, True, True], node = 2, p = 0`                                                                                              |
| `return`                       | `returned = [2, 4, 5, 6]`                                                                                                                                                                 |
