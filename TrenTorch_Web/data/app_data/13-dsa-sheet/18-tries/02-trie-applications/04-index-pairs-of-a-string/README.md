---
name: sheet-index-pairs-of-a-string
title: 'Index Pairs of a String'
tags: [dsa-sheet, tries, trie-applications]
difficulty: Intermediate
---

## Statement

Return all pairs `[start, end]` (inclusive) such that the substring `text[start:end + 1]` is **one of the `words`**. Sort the pairs by `start`, then by `end`. A pair appears once even if the word is in the list twice.

For `text = "thestoryofleetcodeandme"` and `words = ["story", "fleet", "leetcode"]` the answer is `[[3, 7], [9, 13], [10, 17]]`.

The starter code checks every word at every position. It is correct but too slow for many words.

### Examples

**Example 1**

Input:

```python
index_pairs('thestoryofleetcodeandme', ['story', 'fleet', 'leetcode'])
```

Output:

```text
[[3, 7], [9, 13], [10, 17]]
```

**Example 2**

Input:

```python
index_pairs('ababa', ['aba', 'ab'])
```

Output:

```text
[[0, 1], [0, 2], [2, 3], [2, 4]]
```

### Constraints

- `0 <= len(text) <= 100000`
- `0 <= len(words) <= 2000`
- `1 <= len(word) <= 10`, lower-case letters.

## Theory

A **trie** (prefix tree) stores a set of words letter by letter: every node is one letter, a word is a path from the root, and words that share a prefix share the start of their path. Each node has up to 26 children (a dictionary `letter -> node` in Python) and a flag that says "a word ends here". Inserting or searching a word of length `L` takes `O(L)` no matter how many words are stored, and a trie answers **prefix** questions ("does any word start with `ab`?") that a plain set of words cannot answer quickly. A node can be a small dictionary: `node = {}`; mark the end of a word with a special key such as `"$"`.

Put the words in a trie. For each start position `i`, walk the trie along `text[i:]`: every time the node you reach is a word end, record `[i, current index]`. Stop as soon as the walk falls off the trie.

The walk from one start is at most `maxlen` letters long (and usually much shorter), so the total work is `O(len(text) × maxlen)`, independent of the number of words.

## Explanation

`node.get(text[j])` follows one letter; a `"$"` key means a word ends there. The result is sorted as required.
