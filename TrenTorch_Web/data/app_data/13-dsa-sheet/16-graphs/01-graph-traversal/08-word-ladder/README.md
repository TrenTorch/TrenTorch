---
name: sheet-word-ladder
title: 'Word Ladder'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Advanced
---

## Statement

A **word chain** goes from `begin` to `end` where each step changes **exactly one letter** and every word after the first must be in `words`. Return the **number of words in the shortest chain** (`begin` and `end` included), or `0` if there is none. All words have the same length.

For `begin = "hit"`, `end = "cog"` and `words = ["hot", "dot", "dog", "lot", "log", "cog"]` the answer is `5` (`hit -> hot -> dot -> dog -> cog`).

The starter code compares every word with every other word. It is correct but too slow for a long word list.

### Examples

**Example 1**

Input:

```python
ladder_length('hit', 'cog', ['hot', 'dot', 'dog', 'lot', 'log', 'cog'])
```

Output:

```text
5
```

**Explanation:** The end word 'cog' is in the list, and a shortest chain hit->hot->dot->dog->cog has 5 words.

**Example 2**

Input:

```python
ladder_length('hit', 'cog', ['hot', 'dot', 'dog', 'lot', 'log'])
```

Output:

```text
0
```

**Explanation:** The end word 'cog' is missing from the word list, so the function returns 0 immediately.

### Constraints

- `0 <= len(words) <= 5000`
- `1 <= len(word) <= 8`, lower-case letters, all the same length.
- `begin` may or may not be in `words`.

## Theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. Edges can be **undirected** (a road you can use both ways) or **directed** (a one-way street), and they can carry a **weight** (a distance or cost). Two ways to store a graph: an **adjacency list** (for each node, the list of its neighbours; `O(n + m)` memory, the usual choice) or an **adjacency matrix** (an `n x n` table; fast edge lookup but `O(n²)` memory). To visit every node reachable from a start, use **BFS** (a queue, level by level) or **DFS** (a stack or recursion, as deep as possible first). Mark nodes as **visited** so that you never process one twice, otherwise cycles loop forever.

The words are the **nodes**; two words are joined by an edge when they differ in one letter; the chain is a **shortest path**, so use **BFS**.

The expensive part is finding the neighbours of a word: comparing it with all other words costs `O(n·L)` per word. A trick: group the words by **patterns with one wildcard**: `hot` belongs to the groups `*ot`, `h*t` and `ho*`. Two words that differ in one letter share exactly one pattern. Build a dictionary `pattern -> words` once, and the neighbours of a word are the members of its `L` patterns: `O(L)` lookups per word.

Total `O(n·L²)` (with strings of length `L`), instead of `O(n²·L)`.

## Explanation

`groups` maps each wildcard pattern to the words that match it. BFS pops a word, looks up its patterns, and queues the unseen words found there; `steps` counts the words in the chain.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                      | Variables                                                                                                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowed = set(words)`                                               | `allowed = {'dot', 'lot', 'hot', 'cog', 'dog', 'log'}`                                                                                             |
| `for i in range(len(word)):`                                         | `groups = {'*it': ['hit'], 'h*t': ['hit'], 'hi*': ['hit'], '*ot': [..., word = 'lot', i = 0`                                                       |
| `groups.setdefault(word[:i] + "*" + word[i + 1 :], []).append(word)` | `groups = {'*it': ['hit'], 'h*t': ['hit', 'hot'], 'hi*': ['hit'], '..., word = 'hot', i = 1`                                                       |
| `for i in range(len(word)):`                                         | `word = 'hit', i = 2, seen = {'hit', 'hot'}, queue = deque([('hot', 2)]), steps = 1, other = 'hot'`                                                |
| `word, steps = queue.popleft()`                                      | `word = 'dot', seen = {'hit', 'hot', 'lot', 'dot'}, queue = deque([('lot', 3)]), steps = 3`                                                        |
| `for other in groups.get(word[:i] + "*" + word[i + 1 :], ()):`       | `word = 'lot', i = 0, seen = {'dot', 'lot', 'hot', 'hit', 'dog'}, queue = deque([('dog', 4)])`                                                     |
| `for i in range(len(word)):`                                         | `word = 'dog', i = 1, seen = {'dot', 'lot', 'hot', 'cog', 'hit', 'dog', 'log'}, queue = deque([('log', 4), ('cog', 5)]), steps = 4, other = 'log'` |
| `return`                                                             | `returned = 5`                                                                                                                                     |

### Complexity

- Time: O(N * L) with N words, L length.
- Extra space: O(N * L) for groups, queue, and seen.
- The brute force takes O(n^3 * L) n words L length.
