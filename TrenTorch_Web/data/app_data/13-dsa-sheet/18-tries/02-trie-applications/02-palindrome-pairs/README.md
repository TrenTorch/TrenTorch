---
name: sheet-palindrome-pairs
title: 'Palindrome Pairs'
tags: [dsa-sheet, tries, trie-applications]
difficulty: Mastery
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

## Theory

A **trie** (prefix tree) stores a set of words letter by letter: every node is one letter, a word is a path from the root, and words that share a prefix share the start of their path. Each node has up to 26 children (a dictionary `letter -> node` in Python) and a flag that says "a word ends here". Inserting or searching a word of length `L` takes `O(L)` no matter how many words are stored, and a trie answers **prefix** questions ("does any word start with `ab`?") that a plain set of words cannot answer quickly. A node can be a small dictionary: `node = {}`; mark the end of a word with a special key such as `"$"`.

Joining `a + b` is a palindrome when, after matching the start of `a` against the **reverse** of `b`, whatever is left over is itself a palindrome. So for every word `w` and every way to **split it as `prefix + suffix`**:

- if `prefix` is a palindrome and the **reverse of `suffix`** is another word `v` in the list, then `v + w` is a palindrome (v's reverse covers `suffix`, the middle part `prefix` is a palindrome);
- if `suffix` is a palindrome and the **reverse of `prefix`** is a word `v`, then `w + v` is a palindrome.

Store every word in a dictionary `word -> index`, then for each word try its at most `L + 1` splits: `O(n × L²)` instead of `O(n² × L)`. A trie of reversed words does the same job with prefix walks. Be careful with the empty string and with pairs of the same index.

## Explanation

The set `found` avoids duplicates (an empty split can be generated twice). `rev` maps a string to the index of the word equal to it.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                     | Variables                                                                                   |
| ----------------------------------- | ------------------------------------------------------------------------------------------- |
| `index = {}`                        | `index = {}`                                                                                |
| `index.setdefault(w, []).append(i)` | `index = {'abcd': [0], 'dcba': [1], 'lls': [2], 's': [3], 'sssll':..., i = 4, w = 'sssll'`  |
| `prefix, suffix = w[:cut], w[cut:]` | `i = 0, w = 'abcd', found = {(1, 0)}, cut = 2, prefix = 'ab', suffix = 'cd', j = 1`         |
| `for cut in range(len(w) + 1):`     | `i = 1, w = 'dcba', found = {(1, 0), (0, 1)}, cut = 1, prefix = '', suffix = 'dcba', j = 0` |
| `for cut in range(len(w) + 1):`     | `i = 2, w = 'lls', cut = 0, prefix = 'dcba', suffix = ''`                                   |
| `for i, w in enumerate(words):`     | `i = 3, w = 's', found = {(1, 0), (3, 2), (0, 1)}, cut = 3, prefix = 'lls', j = 3`          |
| `for cut in range(len(w) + 1):`     | `i = 4, w = 'sssll', cut = 2, prefix = 's', suffix = 'ssll'`                                |
| `return`                            | `returned = [[0, 1], [1, 0], [2, 4], [3, 2]]`                                               |

### Complexity

- Time: O(n * k^2).
- Extra space: O(n), where n is the number of words. The space is used to store the `index` dictionary, which maps each word to its indices, and the `found` set to track valid pairs. Since only one dictionary and one set are maintained, the space complexity is linear relative to the number of input words.
- The brute force takes O(n^2 * k).
