---
name: sheet-satisfiability-of-equality-equations
title: 'Equality Equations'
tags: [dsa-sheet, graphs, disjoint-sets]
difficulty: Intermediate
---

## Statement

Each string in `equations` has the form `"a==b"` or `"a!=b"`, where `a` and `b` are single lower-case letters (variables). Return `True` if you can give each variable an integer so that **all equations hold**.

For `["a==b", "b!=a"]` the answer is `False`; for `["a==b", "b==c", "a==c"]` it is `True`.

### Examples

**Example 1**

Input:

```python
equations_possible(['a==b', 'b!=a'])
```

Output:

```text
False
```

**Example 2**

Input:

```python
equations_possible(['a==b', 'b==c', 'a==c'])
```

Output:

```text
True
```

### Constraints

- `0 <= len(equations) <= 100000`
- Each equation is 4 characters: a letter, `==` or `!=`, a letter.

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

A **disjoint set union (DSU)**, also called **union-find**, keeps track of a partition of items into groups. It supports two operations: `find(x)` returns the representative (the "leader") of the group of `x`, and `union(a, b)` merges the groups of `a` and `b`. Store a `parent` array where each item points toward its leader. Two tricks make it almost `O(1)` per operation: **path compression** (while walking up in `find`, point nodes closer to the root) and **union by size** (attach the smaller group under the larger). Two items are in the same group exactly when `find(a) == find(b)`.

Equality is **transitive**: if `a == b` and `b == c` then `a == c`. So the `==` equations merge variables into groups of equal values. First process **all** the `==` equations with a union-find. Then check every `!=` equation: if its two variables ended up in the **same** group, it contradicts the equalities: `False`. If no `!=` equation fails, the answer is `True` (give each group its own number).

The order matters: unions first, `!=` checks second. `O(n α)`.

## Explanation

`ord(ch) - 97` maps a letter to a position in `parent`. The two loops do the unions and then the checks.
