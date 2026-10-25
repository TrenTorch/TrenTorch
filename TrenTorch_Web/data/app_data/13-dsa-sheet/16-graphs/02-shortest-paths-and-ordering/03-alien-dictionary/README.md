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

**Explanation:** Comparing adjacent words reveals dependencies like w < e and r < t, and a topological sort with a priority queue produces the lexicographically smallest order.

**Example 2**

Input:

```python
alien_order(['abc', 'ab'])
```

Output:

```text
''
```

**Explanation:** The word 'ab' is a prefix of 'abc', which violates sorting rules where prefixes come first.

### Constraints

- `0 <= len(words) <= 10000`
- `1 <= len(word) <= 20`, lower-case letters.

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

Each pair of **neighbouring words** gives at most one fact: find the first position where they differ; the letter of the first word comes **before** the letter of the second. That is an arrow `x -> y` between letters. (If the second word is a **prefix** of the first, like `"abc"` before `"ab"`, the list is impossible.)

The letters and arrows form a directed graph; the order is a **topological sort**, and the smallest one uses a min-heap with Kahn's algorithm (as in the course order question). If not all letters can be output, there is a cycle: return `""`. Only the neighbouring pairs matter, because "sorted" is transitive.

## Explanation

`edges` is a set of `(x, y)` pairs, so repeated facts count once. The in-degree counts only distinct arrows.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                       | Variables                                                                                                                                               |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `letters = sorted({ch for w in words for ch in w})`   | `letters = ['e', 'f', 'r', 't', 'w']`                                                                                                                   |
| `for x, y in zip(a, b):`                              | `edges = {('t', 'f')}, a = 'wrf', b = 'er', x = 'w', y = 'e'`                                                                                           |
| `edges.add((x, y))`                                   | `edges = {('r', 't'), ('e', 'r'), ('w', 'e'), ('t', 'f')}, a = 'ett', b = 'rftt', x = 'e', y = 'r'`                                                     |
| `in_degree[y] += 1`                                   | `adj = {'e': ['r'], 'f': [], 'r': ['t'], 't': [], 'w': []}, in_degree = {'e': 0, 'f': 0, 'r': 1, 't': 1, 'w': 0}`                                       |
| `heap = [ch for ch in letters if in_degree[ch] == 0]` | `x = 't', y = 'f', adj = {'e': ['r'], 'f': [], 'r': ['t'], 't': ['f'], 'w': ['e']}, in_degree = {'e': 1, 'f': 1, 'r': 1, 't': 1, 'w': 0}, heap = ['w']` |
| `out.append(ch)`                                      | `in_degree = {'e': 0, 'f': 1, 'r': 1, 't': 1, 'w': 0}, heap = [], out = ['w', 'e'], ch = 'e', nxt = 'e'`                                                |
| `heapq.heappush(heap, nxt)`                           | `in_degree = {'e': 0, 'f': 1, 'r': 0, 't': 0, 'w': 0}, heap = ['t'], out = ['w', 'e', 'r'], ch = 'r', nxt = 't'`                                        |
| `return`                                              | `returned = 'wertf'`                                                                                                                                    |

### Complexity

- Time: O(n + q).
- Extra space: O(U) where U is the number of unique characters.
- The brute force takes O(n!).
