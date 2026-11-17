---
name: sheet-count-words-with-prefix
title: 'Count Words With a Prefix'
tags: [dsa-sheet, tries, trie-basics]
difficulty: Beginner
theory: answering-many-prefix-queries
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

## Explanation

`node["#"]` counts the words through the node. The query walk ends in the node whose counter is returned.

### Complexity

- Time: O(W + Q). `W` is the total length of the words and `Q` the total length of the queries: each letter is stepped once.
- Space: O(W). One trie node per letter, each with a counter.
