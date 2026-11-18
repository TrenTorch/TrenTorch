---
name: sheet-implement-trie
title: 'Implement a Trie'
tags: [dsa-sheet, tries, trie-basics]
difficulty: Beginner
theory: search-and-starts-with
---

## Statement

Build a trie and run a list of operations on it, starting empty. Each operation is a string: `"insert w"` adds the word `w`, `"search w"` asks whether the **whole word** `w` was inserted, and `"starts w"` asks whether **some inserted word starts with** `w`. Return the answers of all `search` and `starts` operations, in order, as booleans.

For `["insert apple", "search apple", "search app", "starts app", "insert app", "search app"]` the answer is `[True, False, True, True]`.

### Examples

**Example 1**

Input:

```python
run_trie(['insert apple', 'search apple', 'search app', 'starts app', 'insert app', 'search app'])
```

Output:

```text
[True, False, True, True]
```

**Example 2**

Input:

```python
run_trie([])
```

Output:

```text
[]
```

### Constraints

- `0 <= len(ops) <= 100000`
- Words are lower-case letters, 1 to 20 long.

## Explanation

`walk(word)` returns the node reached by the word, or `None`. `search` also checks the end marker `"$"`.

### Complexity

- Time: O(L) per operation. Each insert, search or prefix check walks one letter at a time, `L` = length of the word; the total is the sum of all word lengths.
- Space: O(T). `T` is the total length of the inserted words (one trie node per new letter).
