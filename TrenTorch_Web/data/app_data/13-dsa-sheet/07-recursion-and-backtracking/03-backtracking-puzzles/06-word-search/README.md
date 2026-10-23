---
name: sheet-word-search
title: 'Word Search'
tags: [dsa-sheet, recursion, backtracking-puzzles]
difficulty: Intermediate
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

## Theory

Try every cell as the **start**. From a cell that matches the first letter, explore its four neighbours for the next letter, and so on: a **depth-first search** that backtracks when a letter does not match.

To stop a path from reusing a cell, **mark it as visited** before exploring further and **unmark it when you come back** (that is the backtracking step). A simple way is to temporarily replace the cell's letter by a marker such as `"#"` that matches nothing.

Prune early: if the current cell's letter is not the wanted one, return `False` immediately. The cost is about `rows * cols * 3^len(word)` in the worst case, since each step has at most 3 new directions.

## Explanation

`go(r, c, i)` checks whether the word from index `i` can be spelled starting at cell `(r, c)`. It fails if the cell is out of range, already used, or the wrong letter. It marks the cell, tries the four neighbours, and restores the cell before returning.
