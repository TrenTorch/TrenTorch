---
name: sheet-index-pairs-of-a-string
title: 'Index Pairs of a String'
tags: [dsa-sheet, tries, trie-applications]
difficulty: Intermediate
theory: all-stored-words-that-start-at-a-position
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

## Explanation

`node.get(text[j])` follows one letter; a `"$"` key means a word ends there. The result is sorted as required.

### Complexity

- Time: O(W + n * L + Z). `W` = total length of the words, `L` = longest word, `Z` = number of pairs found: each start position walks down the trie at most `L` letters.
- Space: O(W + Z). The trie and the output.
