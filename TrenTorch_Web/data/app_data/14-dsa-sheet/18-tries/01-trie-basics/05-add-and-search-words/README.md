---
name: sheet-add-and-search-words
title: 'Add and Search Words With Wildcards'
tags: [dsa-sheet, tries, trie-basics]
difficulty: Intermediate
theory: how-slow-can-it-get
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

## Explanation

`go` returns as soon as one branch succeeds. The key `"$"` is skipped when iterating the children of a `.`.

### Complexity

- Time: O(L) to add; O(L) to search, up to O(T) with dots. A search without `.` follows one path; every `.` branches into all children, so the worst case visits the whole trie (`T` nodes).
- Space: O(T). One trie node per stored letter.
