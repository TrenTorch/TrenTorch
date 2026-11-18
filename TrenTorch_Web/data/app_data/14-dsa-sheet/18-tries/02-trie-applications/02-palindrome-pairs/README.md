---
name: sheet-palindrome-pairs
title: 'Palindrome Pairs'
tags: [dsa-sheet, tries, trie-applications]
difficulty: Mastery
theory: putting-the-pairs-together
---

## Statement

Return all pairs of **different indices** `[i, j]` such that `words[i] + words[j]` (joined in that order) is a **palindrome**. List the pairs sorted (by `i`, then `j`).

For `["abcd", "dcba", "lls", "s", "sssll"]` the answer is `[[0, 1], [1, 0], [2, 4], [3, 2]]`.

The starter code tests every pair. It is correct but too slow for many words.

### Examples

**Example 1**

Input:

```python
palindrome_pairs(['abcd', 'dcba', 'lls', 's', 'sssll'])
```

Output:

```text
[[0, 1], [1, 0], [2, 4], [3, 2]]
```

**Example 2**

Input:

```python
palindrome_pairs(['bat', 'tab', 'cat'])
```

Output:

```text
[[0, 1], [1, 0]]
```

### Constraints

- `0 <= len(words) <= 3000`
- `0 <= len(word) <= 12`, lower-case letters; words may repeat and may be empty.

## Explanation

The set `found` avoids duplicates (an empty split can be generated twice). `rev` maps a string to the index of the word equal to it.

### Complexity

- Time: O(n * k^2 + P log P). `k` = longest word: for each word and each cut, a palindrome check and a hash lookup of a reversed piece cost O(k); `P` pairs are sorted for the output.
- Space: O(n * k). The table of words and the set of pairs.
