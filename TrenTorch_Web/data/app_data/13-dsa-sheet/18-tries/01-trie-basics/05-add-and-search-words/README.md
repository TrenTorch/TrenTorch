---
name: sheet-add-and-search-words
title: 'Add and Search Words With Wildcards'
tags: [dsa-sheet, tries, trie-basics]
difficulty: Intermediate
---

## Statement

Build a word dictionary. Each operation is a string: `"add w"` stores the word `w`; `"search p"` asks whether some stored word **matches the pattern `p`**, where `.` matches **any single letter** and every other character matches itself (the word and the pattern must have the same length). Return the answers of all `search` operations, in order.

For `["add bad", "add dad", "add mad", "search pad", "search bad", "search .ad", "search b.."]` the answer is `[False, True, True, True]`.

### Examples

**Example 1**

Input:

```python
run_word_dictionary(['add bad', 'add dad', 'add mad', 'search pad', 'search bad', 'search .ad', 'search b..'])
```

Output:

```text
[False, True, True, True]
```

**Example 2**

Input:

```python
run_word_dictionary(['search a'])
```

Output:

```text
[False]
```

### Constraints

- `0 <= len(ops) <= 20000`
- Words and patterns are lower-case letters (patterns also `.`), 1 to 12 long.

## Theory

A **trie** (prefix tree) stores a set of words letter by letter: every node is one letter, a word is a path from the root, and words that share a prefix share the start of their path. Each node has up to 26 children (a dictionary `letter -> node` in Python) and a flag that says "a word ends here". Inserting or searching a word of length `L` takes `O(L)` no matter how many words are stored, and a trie answers **prefix** questions ("does any word start with `ab`?") that a plain set of words cannot answer quickly. A node can be a small dictionary: `node = {}`; mark the end of a word with a special key such as `"$"`.

A search with a wildcard cannot follow one path: at a `.` **every child** is a possibility. Use a recursive DFS `go(node, i)`: if `i` is the end of the pattern, the answer is whether `node` is a word end; if the pattern letter is a normal letter, follow that child only (if it exists); if it is `.`, try every child and return `True` if any of them works.

The cost of a pattern with many dots can be larger than the pattern length, but it never exceeds the size of the trie.

## Explanation

`go` returns as soon as one branch succeeds. The key `"$"` is skipped when iterating the children of a `.`.
