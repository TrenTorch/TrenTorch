---
name: sheet-implement-trie
title: 'Implement a Trie'
tags: [dsa-sheet, tries, trie-basics]
difficulty: Beginner
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

## Theory

A **trie** (prefix tree) stores a set of words letter by letter: every node is one letter, a word is a path from the root, and words that share a prefix share the start of their path. Each node has up to 26 children (a dictionary `letter -> node` in Python) and a flag that says "a word ends here". Inserting or searching a word of length `L` takes `O(L)` no matter how many words are stored, and a trie answers **prefix** questions ("does any word start with `ab`?") that a plain set of words cannot answer quickly. A node can be a small dictionary: `node = {}`; mark the end of a word with a special key such as `"$"`.

Insert: walk from the root, creating a child node for each letter that is missing; at the end mark the node as a word end. Search: walk the same way; the word is present if every letter exists **and** the last node is marked as a word end. Prefix test: only the path must exist. The difference between `search` and `starts` is the end marker: in the example, `app` is a prefix of `apple` but not a word until it is inserted itself.

## Explanation

`walk(word)` returns the node reached by the word, or `None`. `search` also checks the end marker `"$"`.
