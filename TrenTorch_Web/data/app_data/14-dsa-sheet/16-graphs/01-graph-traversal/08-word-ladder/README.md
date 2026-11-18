---
name: sheet-word-ladder
title: 'Word Ladder'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Advanced
theory: graphs-made-from-a-rule-word-ladder
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

**Example 2**

Input:

```python
ladder_length('hit', 'cog', ['hot', 'dot', 'dog', 'lot', 'log'])
```

Output:

```text
0
```

### Constraints

- `0 <= len(words) <= 5000`
- `1 <= len(word) <= 8`, lower-case letters, all the same length.
- `begin` may or may not be in `words`.

## Explanation

`groups` maps each wildcard pattern to the words that match it. BFS pops a word, looks up its patterns, and queues the unseen words found there; `steps` counts the words in the chain.

### Complexity

- Time: O(N * L^2). `N` words of length `L`: every word is put in `L` pattern groups, each costing `O(L)` to build, and the search visits each word once.
- Space: O(N * L^2). The pattern groups hold `N * L` strings of length `L`.
