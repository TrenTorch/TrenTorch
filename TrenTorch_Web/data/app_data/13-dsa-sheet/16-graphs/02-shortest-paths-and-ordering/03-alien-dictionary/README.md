---
name: sheet-alien-dictionary
title: 'Alien Dictionary'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Mastery
---

## Statement

An alien language uses the lower-case letters in an unknown alphabetical order. `words` is a list of words **sorted in that language's order**. Return a string with **every letter that appears in the words**, in an order that is consistent with the list. If several orders fit, return the **lexicographically smallest** (in normal English order). If no order fits (a contradiction, or a longer word placed before its own prefix), return `""`.

For `["wrt", "wrf", "er", "ett", "rftt"]` the answer is `"wertf"`.

### Examples

**Example 1**

Input:

```python
alien_order(['wrt', 'wrf', 'er', 'ett', 'rftt'])
```

Output:

```text
'wertf'
```

**Example 2**

Input:

```python
alien_order(['abc', 'ab'])
```

Output:

```text
''
```

### Constraints

- `0 <= len(words) <= 10000`
- `1 <= len(word) <= 20`, lower-case letters.

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

Each pair of **neighbouring words** gives at most one fact: find the first position where they differ; the letter of the first word comes **before** the letter of the second. That is an arrow `x -> y` between letters. (If the second word is a **prefix** of the first, like `"abc"` before `"ab"`, the list is impossible.)

The letters and arrows form a directed graph; the order is a **topological sort**, and the smallest one uses a min-heap with Kahn's algorithm (as in the course order question). If not all letters can be output, there is a cycle: return `""`. Only the neighbouring pairs matter, because "sorted" is transitive.

## Explanation

`edges` is a set of `(x, y)` pairs, so repeated facts count once. The in-degree counts only distinct arrows.
