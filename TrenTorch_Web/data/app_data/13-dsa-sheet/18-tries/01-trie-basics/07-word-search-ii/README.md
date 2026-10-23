---
name: sheet-word-search-ii
title: 'Word Search II'
tags: [dsa-sheet, tries, trie-basics]
difficulty: Mastery
---

## Statement

`board` is a grid of letters (a list of equal-length strings). A word can be traced by walking between **neighbouring cells** (up, down, left, right), using **each cell at most once** per word. Return the **different words from `words` that can be traced**, sorted.

For `board = ["oaan", "etae", "ihkr", "iflv"]` and `words = ["oath", "pea", "eat", "rain"]` the answer is `["eat", "oath"]`.

The starter code runs a separate board search for every word. It is correct but too slow for many words.

### Examples

**Example 1**

Input:

```python
find_words(['oaan', 'etae', 'ihkr', 'iflv'], ['oath', 'pea', 'eat', 'rain'])
```

Output:

```text
['eat', 'oath']
```

**Example 2**

Input:

```python
find_words(['ab', 'cd'], ['abcb'])
```

Output:

```text
[]
```

### Constraints

- `0 <= rows, cols <= 8`
- `0 <= len(words) <= 3000`
- Lower-case letters; words are 1 to 10 long.

## Theory

A **trie** (prefix tree) stores a set of words letter by letter: every node is one letter, a word is a path from the root, and words that share a prefix share the start of their path. Each node has up to 26 children (a dictionary `letter -> node` in Python) and a flag that says "a word ends here". Inserting or searching a word of length `L` takes `O(L)` no matter how many words are stored, and a trie answers **prefix** questions ("does any word start with `ab`?") that a plain set of words cannot answer quickly. A node can be a small dictionary: `node = {}`; mark the end of a word with a special key such as `"$"`.

Searching the board once **for each word** repeats the same paths: many words share prefixes. Put all the words in a trie, then run **one backtracking search** from every cell, walking the board and the trie together: from a cell, only continue into a neighbour if the trie has a child for its letter.

When the trie node you stand on marks a word end, record the word (and unmark it so it is found once). The trie prunes any path that is a prefix of no word, so the search is far smaller than one search per word. Remember to **mark the cell as used and restore it** when you backtrack.

## Explanation

`dfs(r, c, node)` follows the board letter into the trie. The cell is blanked during the recursion and restored afterwards.
