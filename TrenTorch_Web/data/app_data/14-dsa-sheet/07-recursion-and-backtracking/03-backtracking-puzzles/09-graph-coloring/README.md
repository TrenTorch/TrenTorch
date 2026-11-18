---
name: sheet-graph-coloring
title: 'Can the Graph Be Coloured?'
tags: [dsa-sheet, recursion, backtracking-puzzles]
difficulty: Advanced
theory: colouring-a-graph
---

## Statement

A graph has `n` nodes numbered `0` to `n - 1` and some `edges`, each `[u, v]` joining two nodes. Return `True` if every node can be given one of `colors` colours so that **the two ends of every edge have different colours**. An edge from a node to itself (`u == v`) can never be coloured, so the answer is then `False`.

### Examples

**Example 1**

Input:

```python
can_color_graph(3, [[0, 1], [1, 2], [0, 2]], 3)
```

Output:

```text
True
```

**Example 2**

Input:

```python
can_color_graph(3, [[0, 1], [1, 2], [0, 2]], 2)
```

Output:

```text
False
```

### Constraints

- `0 <= n <= 14`
- `0 <= len(edges) <= 40`
- `0 <= u, v < n`
- `1 <= colors <= 5`

## Explanation

`adj[i]` lists the neighbours of `i`. `go(i)` tries every colour not used by an already-coloured neighbour; a successful full assignment returns `True`, and failing colours are reset to `-1` (uncoloured) before the next try. A self-loop makes the answer `False` immediately.

### Complexity

- Time: O(k^n * (n + e)). Each vertex tries up to `k` colours (`k` = colors) and checks its neighbours; the problem is NP-complete in general, so no polynomial-time method is known.
- Space: O(n + e). The adjacency lists and the colour array.
