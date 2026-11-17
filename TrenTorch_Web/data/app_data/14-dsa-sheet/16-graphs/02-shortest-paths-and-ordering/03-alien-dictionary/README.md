---
name: sheet-alien-dictionary
title: 'Alien Dictionary'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Mastery
theory: alien-dictionary
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

## Explanation

`edges` is a set of `(x, y)` pairs, so repeated facts count once. The in-degree counts only distinct arrows.

### Complexity

- Time: O(S + L log L + e). `S` is the total number of characters: comparing neighbouring words gives at most one edge per pair; then a heap-based topological sort over the `L` distinct letters.
- Space: O(L + e). The graph over at most 26 letters.
