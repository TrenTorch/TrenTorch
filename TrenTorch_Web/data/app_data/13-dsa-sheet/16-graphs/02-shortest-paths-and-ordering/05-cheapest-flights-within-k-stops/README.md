---
name: sheet-cheapest-flights-within-k-stops
title: 'Cheapest Flights Within K Stops'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Advanced
---

## Statement

There are `n` cities and flights `[from, to, price]` (one-way). Return the **cheapest price** to travel from `src` to `dst` with **at most `k` stops** in between (so at most `k + 1` flights), or `-1` if impossible.

For `n = 4`, `flights = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]`, `src = 0`, `dst = 3` and `k = 1` the answer is `700`.

### Examples

**Example 1**

Input:

```python
cheapest_price(4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1)
```

Output:

```text
700
```

**Example 2**

Input:

```python
cheapest_price(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0)
```

Output:

```text
500
```

### Constraints

- `1 <= n <= 1000`
- `0 <= len(flights) <= 5000`
- `0 <= price <= 10**4`
- `0 <= k <= n`

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

Plain Dijkstra picks the cheapest route, but here a limit on the **number of edges** matters: the cheapest route may use too many stops, and a more expensive route with fewer stops may be the only valid one. So the state must include the number of flights used.

**Bellman–Ford with a round limit** handles it: let `best[v]` be the cheapest known price to reach `v`. Run `k + 1` rounds; in each round, relax every flight **using the values from the previous round only** (copy the array first), so that each round adds exactly one more flight to any path. After `k + 1` rounds, `best[dst]` is the answer. `O(k · m)`.

The copy is the trap: without it, one round could chain several flights and break the stop limit.

## Explanation

`nxt` starts as a copy of `best`. Each flight is relaxed from the old `best`, so a path gains at most one flight per round.
