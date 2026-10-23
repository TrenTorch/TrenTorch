---
name: sheet-count-words-with-prefix
title: 'Count Words With a Prefix'
tags: [dsa-sheet, tries, trie-basics]
difficulty: Beginner
---

## Statement

Given `words` and a list of `queries` (prefixes), return for **each query the number of words that start with it** (a word equal to the query counts). Repeated words count each time.

For `words = ["apple", "app", "apt", "bat"]` and `queries = ["ap", "app", "b", "c"]` the answer is `[3, 2, 1, 0]`.

The starter code checks every word for every query. It is correct but too slow for many words and queries.

### Examples

**Example 1**

Input:

```python
count_with_prefix(['apple', 'app', 'apt', 'bat'], ['ap', 'app', 'b', 'c'])
```

Output:

```text
[3, 2, 1, 0]
```

**Example 2**

Input:

```python
count_with_prefix([], ['a'])
```

Output:

```text
[0]
```

### Constraints

- `0 <= len(words), len(queries) <= 50000`
- `1 <= length <= 12`, lower-case letters.

## Theory

A **trie** (prefix tree) stores a set of words letter by letter: every node is one letter, a word is a path from the root, and words that share a prefix share the start of their path. Each node has up to 26 children (a dictionary `letter -> node` in Python) and a flag that says "a word ends here". Inserting or searching a word of length `L` takes `O(L)` no matter how many words are stored, and a trie answers **prefix** questions ("does any word start with `ab`?") that a plain set of words cannot answer quickly. A node can be a small dictionary: `node = {}`; mark the end of a word with a special key such as `"$"`.

Store in every trie node the **number of words that pass through it**. When inserting a word, increase the counter of every node on its path. A query is then a walk along the prefix; the counter of the last node is the answer (or 0 if the walk falls off the trie).

Building costs `O(total letters)`, each query `O(len(query))`, independent of the number of words. Checking every word for each query costs `O(words × queries)`.

## Explanation

`node["#"]` counts the words through the node. The query walk ends in the node whose counter is returned.
