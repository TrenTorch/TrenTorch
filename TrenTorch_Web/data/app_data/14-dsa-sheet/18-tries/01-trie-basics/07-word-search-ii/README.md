---
name: sheet-word-search-ii
title: 'Word Search II'
tags: [dsa-sheet, tries, trie-basics]
difficulty: Mastery
theory: why-the-search-stays-fast
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

## Explanation

`dfs(r, c, node)` follows the board letter into the trie. The cell is blanked during the recursion and restored afterwards.

### Complexity

- Time: O(r * c * 3^L + W). One depth-first search from every cell that follows the trie, so a branch stops as soon as no word continues that way (`L` = longest word, `W` = total length of the words).
- Space: O(W + r * c). The trie and the working copy of the board.
