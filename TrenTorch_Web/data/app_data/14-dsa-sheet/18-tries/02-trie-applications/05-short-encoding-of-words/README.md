---
name: sheet-short-encoding-of-words
title: 'Short Encoding of Words'
tags: [dsa-sheet, tries, trie-applications]
difficulty: Advanced
theory: a-word-hiding-at-the-end-of-another
---

## Statement

A set of words is **encoded** by one string `s` that ends with `#` after each word's position: every word `w` must appear in `s` starting at some index `i` and **ending just before a `#`**. So `"time#bell#"` encodes `["time", "bell"]`, and `"time#"` encodes both `"time"` and `"me"` (since `"me"` ends right before the `#` as well). Return the **length of the shortest** such string `s`.

For `["time", "me", "bell"]` the answer is `10` (`"time#bell#"`).

### Examples

**Example 1**

Input:

```python
minimum_length_encoding(['time', 'me', 'bell'])
```

Output:

```text
10
```

**Example 2**

Input:

```python
minimum_length_encoding(['t'])
```

Output:

```text
2
```

### Constraints

- `0 <= len(words) <= 20000`
- `1 <= len(word) <= 7`, lower-case letters.

## Explanation

A word needs its own place in the encoding only if it is not a suffix of another word. Insert every distinct word into a trie letter by letter from its END: a word that is a suffix of another one ends inside the other's path, so its node has children. A word whose node is a leaf is not a suffix of any other, and it costs `len(word) + 1` (the `#`).

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                  | Variables                                                                                                       |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `trie = {}`                      | `trie = {}`                                                                                                     |
| `for ch in reversed(word):`      | `ends = [], word = 'bell', node = {}, ch = 'l'`                                                                 |
| `for ch in reversed(word):`      | `trie = {'l': {'l': {'e': {}}}}, ch = 'b'`                                                                      |
| `node = trie`                    | `trie = {'l': {'l': {'e': {'b': {}}}}}, ends = [({}, 4)], word = 'time', node = {'l': {'l': {'e': {'b': {}}}}}` |
| `node = node.setdefault(ch, {})` | `trie = {'l': {'l': {'e': {'b': {}}}}, 'e': {'m': {}}}, node = {}, ch = 'm'`                                    |
| `node = node.setdefault(ch, {})` | `trie = {'l': {'l': {'e': {'b': {}}}}, 'e': {'m': {'i': {'t': {}}}}}, ch = 't'`                                 |
| `node = node.setdefault(ch, {})` | `ends = [({}, 4), ({}, 4)], word = 'me', node = {'m': {'i': {'t': {}}}}, ch = 'e'`                              |
| `return`                         | `returned = 10`                                                                                                 |

### Complexity

- Time: O(S). `S` is the total length of the words: every word is put into a trie of reversed words once; a word that ends at a leaf is not a suffix of another.
- Space: O(S). The trie.
