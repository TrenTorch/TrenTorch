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

**Explanation:** The words "eat" and "oath" can be formed by moving between adjacent cells without reusing a cell, while "pea" and "rain" cannot be matched on the given grid, so the output is ["eat", "oath"].

**Example 2**

Input:

```python
find_words(['ab', 'cd'], ['abcb'])
```

Output:

```text
[]
```

**Explanation:** On the 2x2 board "ab","cd" the word "abcb" requires the cell containing "b" to be visited twice, which is prohibited, so no word is found and the output is []

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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line         | Variables                                                                                                                                                                                   |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rows = len(board)`     | `rows = 4`                                                                                                                                                                                  |
| `for ch in word:`       | `cols = 4, trie = {'o': {'a': {}}}, word = 'oath', node = {}, ch = 't'`                                                                                                                     |
| `for ch in word:`       | `trie = {'o': {'a': {'t': {'h': {'$': 'oath'}}}}, 'p': {}}, word = 'pea', ch = 'e'`                                                                                                         |
| `for ch in word:`       | `trie = {'o': {'a': {'t': {'h': {'$': 'oath'}}}}, 'p': {'e': {'a'..., word = 'eat', ch = 'a'`                                                                                               |
| `for ch in word:`       | `word = 'rain', ch = 'n'`                                                                                                                                                                   |
| `for c in range(cols):` | `node = {'$': 'rain'}, grid = [['o', 'a', 'a', 'n'], ['e', 't', 'a', 'e'], ['i', 'h', '..., found = {'oath'}, dfs = <function find_words.<locals>.dfs at 0x000001F48329C820>, r = 0, c = 2` |
| `for c in range(cols):` | `found = {'oath', 'eat'}, r = 2, c = 0`                                                                                                                                                     |
| `return`                | `returned = ['eat', 'oath']`                                                                                                                                                                |
