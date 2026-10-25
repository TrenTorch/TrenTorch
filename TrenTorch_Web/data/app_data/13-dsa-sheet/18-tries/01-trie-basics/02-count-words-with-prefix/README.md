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

**Explanation:** The prefix "ap" matches "apple", "app", and "apt", giving 3; "app" matches "apple" and "app", giving 2; "b" matches "bat", giving 1; "c" matches none, giving 0.

**Example 2**

Input:

```python
count_with_prefix([], ['a'])
```

Output:

```text
[0]
```

**Explanation:** With no words, any prefix, including "a", matches zero words, so the result is [0].

### Constraints

- `0 <= len(words), len(queries) <= 50000`
- `1 <= length <= 12`, lower-case letters.

## Theory

A **trie** (prefix tree) stores a set of words letter by letter: every node is one letter, a word is a path from the root, and words that share a prefix share the start of their path. Each node has up to 26 children (a dictionary `letter -> node` in Python) and a flag that says "a word ends here". Inserting or searching a word of length `L` takes `O(L)` no matter how many words are stored, and a trie answers **prefix** questions ("does any word start with `ab`?") that a plain set of words cannot answer quickly. A node can be a small dictionary: `node = {}`; mark the end of a word with a special key such as `"$"`.

Store in every trie node the **number of words that pass through it**. When inserting a word, increase the counter of every node on its path. A query is then a walk along the prefix; the counter of the last node is the answer (or 0 if the walk falls off the trie).

Building costs `O(total letters)`, each query `O(len(query))`, independent of the number of words. Checking every word for each query costs `O(words × queries)`.

## Explanation

`node["#"]` counts the words through the node. The query walk ends in the node whose counter is returned.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                    | Variables                                                                                                                                                          |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `root = {"#": 0}`                                  | `root = {'#': 0}`                                                                                                                                                  |
| `for ch in word:`                                  | `root = {'#': 0, 'a': {'#': 1, 'p': {'#': 1, 'p': {'#': 1}}}}, word = 'apple', node = {'#': 1}, ch = 'l'`                                                          |
| `node["#"] += 1`                                   | `root = {'#': 0, 'a': {'#': 2, 'p': {'#': 1, 'p': {'#': 1, 'l': {..., word = 'app', node = {'#': 2, 'p': {'#': 1, 'p': {'#': 1, 'l': {'#': 1, 'e': {..., ch = 'a'` |
| `for ch in word:`                                  | `root = {'#': 0, 'a': {'#': 3, 'p': {'#': 2, 'p': {'#': 2, 'l': {..., word = 'apt', node = {'#': 3, 'p': {'#': 2, 'p': {'#': 2, 'l': {'#': 1, 'e': {..., ch = 'p'` |
| `for ch in word:`                                  | `root = {'#': 0, 'a': {'#': 3, 'p': {'#': 3, 'p': {'#': 2, 'l': {..., word = 'bat', node = {'#': 1}, ch = 'a'`                                                     |
| `for ch in q:`                                     | `node = {'#': 3, 'p': {'#': 3, 'p': {'#': 2, 'l': {'#': 1, 'e': {..., ch = 'p', out = [], q = 'ap'`                                                                |
| `out.append(node["#"] if node is not None else 0)` | `node = {'#': 2, 'l': {'#': 1, 'e': {'#': 1}}}, out = [3, 2], q = 'app'`                                                                                           |
| `return`                                           | `returned = [3, 2, 1, 0]`                                                                                                                                          |

### Complexity

- Time: O(n + q) where n = total word chars, q = total query chars.
- Extra space: O(n) where n = total word chars.
- The brute force takes O(n * q) where n = number of words, q = number of queries.
