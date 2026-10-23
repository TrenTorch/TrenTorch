---
name: sheet-suffix-array
title: 'Suffix Array'
tags: [dsa-sheet, advanced-strings, hashing-and-structure]
difficulty: Mastery
---

## Statement

The **suffix array** of `s` lists the starting positions of all its suffixes, in the **dictionary order of the suffixes**. For `"banana"` the suffixes sorted are `a, ana, anana, banana, na, nana` (starting at 5, 3, 1, 0, 4, 2), so the answer is `[5, 3, 1, 0, 4, 2]`.

### Examples

**Example 1**

Input:

```python
suffix_array('banana')
```

Output:

```text
[5, 3, 1, 0, 4, 2]
```

**Example 2**

Input:

```python
suffix_array('aaaa')
```

Output:

```text
[3, 2, 1, 0]
```

### Constraints

- `0 <= len(s) <= 10000`
- Lower-case letters.

## Theory

Sorting the suffixes as strings, `sorted(range(n), key=lambda i: s[i:])`, builds `n` strings of total length `n²/2`, which is too much memory and time for long strings.

**Prefix doubling:** give every suffix a rank based on its first `k` letters (start with `k = 1`: the rank of the letter). Then sort the suffixes by the pair `(rank[i], rank[i + k])`, which orders them by their first `2k` letters, and renumber the ranks. Repeat with `k = 2, 4, 8, ...` until all ranks are different or `k >= n`. That is `O(log n)` rounds, each a sort of `n` pairs: `O(n log² n)`.

The suffix array together with the **LCP array** (longest common prefix of neighbours) solves many string questions: number of distinct substrings, longest repeated substring, pattern search by binary search.

## Explanation

`rank[i + k]` is `-1` past the end, so shorter suffixes sort first. After sorting, equal pairs get equal ranks.
