---
name: sheet-word-search
title: 'Word Search'
tags: [dsa-sheet, recursion, backtracking-puzzles]
difficulty: Intermediate
theory: hunting-for-a-word-in-a-grid
---

## Statement

`board` is a grid of letters given as a list of equal-length strings. Return `True` if `word` can be spelled by walking from cell to **neighbouring** cell (up, down, left or right), where **each cell is used at most once** in the path.

### Examples

**Example 1**

Input:

```python
word_search(['abce', 'sfcs', 'adee'], 'abcced')
```

Output:

```text
True
```

**Example 2**

Input:

```python
word_search(['abce', 'sfcs', 'adee'], 'abcb')
```

Output:

```text
False
```

### Constraints

- `0 <= rows, cols <= 6`
- `0 <= len(word) <= 12`
- Lower-case letters. The empty word is always found.

## Explanation

`go(r, c, i)` checks whether the word from index `i` can be spelled starting at cell `(r, c)`. It fails if the cell is out of range, already used, or the wrong letter. It marks the cell, tries the four neighbours, and restores the cell before returning.

### Complexity

- Time: O(r * c * 3^L). A search starts at every cell and, after the first step, has at most 3 new directions per letter of the word (`L` letters).
- Space: O(r * c + L). The working copy of the board and the recursion.
