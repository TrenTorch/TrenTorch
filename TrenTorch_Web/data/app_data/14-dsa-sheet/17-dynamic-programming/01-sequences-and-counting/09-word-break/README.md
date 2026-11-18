---
name: sheet-word-break
title: 'Word Break'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Intermediate
theory: perfect-squares-and-word-break
---

## Statement

Return `True` if the string `s` can be **split into a sequence of words from `words`** (words may be reused any number of times).

For `s = "leetcode"` and `words = ["leet", "code"]` the answer is `True`; for `s = "catsandog"` and `words = ["cats", "dog", "sand", "and", "cat"]` it is `False`.

The starter code tries every split without remembering failures. It is correct but too slow on strings that cannot be split.

### Examples

**Example 1**

Input:

```python
word_break('leetcode', ['leet', 'code'])
```

Output:

```text
True
```

**Example 2**

Input:

```python
word_break('catsandog', ['cats', 'dog', 'sand', 'and', 'cat'])
```

Output:

```text
False
```

### Constraints

- `0 <= len(s) <= 20000`
- `0 <= len(words) <= 1000`
- `1 <= len(word) <= 20`, lower-case letters.

## Explanation

Put all words in a trie (a tree with one letter per edge and a marker where a word ends). `reachable[i]` says the string can be split up to position `i`. From every reachable `i`, walk down the trie along `s[i], s[i+1], ...`: each time you pass a word-end marker at position `j`, mark `reachable[j + 1]`. The walk stops as soon as the next letter is not in the trie, so it is at most the longest word long.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                    | Variables                                                                                                                                                                             |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `trie = {}`                        | `trie = {}`                                                                                                                                                                           |
| `node = node.setdefault(ch, {})`   | `trie = {'l': {'e': {'e': {}}}}, word = 'leet', node = {}, ch = 'e'`                                                                                                                  |
| `for ch in word:`                  | `trie = {'l': {'e': {'e': {'t': {None: True}}}}, 'c': {}}, word = 'code', ch = 'o'`                                                                                                   |
| `reachable = [True] + [False] * n` | `trie = {'l': {'e': {'e': {'t': {None: True}}}}, 'c': {'o': {'d':..., node = {None: True}, ch = 'e', n = 8, reachable = [True, False, False, False, False, False, False, False, F...` |
| `node = node.get(s[j])`            | `node = {'t': {None: True}}, i = 0, j = 2`                                                                                                                                            |
| `for i in range(n):`               | `node = None, reachable = [True, False, False, False, True, False, False, False, Fa..., i = 2, j = 4`                                                                                 |
| `node = node.get(s[j])`            | `node = {'e': {None: True}}, i = 4, j = 6`                                                                                                                                            |
| `return`                           | `returned = True`                                                                                                                                                                     |

### Complexity

- Time: O(n * L + W). Every start position that can be reached walks down a trie of the words at most `L` letters (`L` = longest word); building the trie costs the total length `W` of all words.
- Space: O(W + n). The trie and the table of reachable positions.
