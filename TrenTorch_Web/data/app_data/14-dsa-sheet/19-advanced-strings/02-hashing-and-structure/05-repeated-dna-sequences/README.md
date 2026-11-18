---
name: sheet-repeated-dna-sequences
title: 'Repeated DNA Sequences'
tags: [dsa-sheet, advanced-strings, hashing-and-structure]
difficulty: Intermediate
theory: fixed-size-windows-repeated-dna-sequences
---

## Statement

A DNA string uses the letters `A`, `C`, `G`, `T`. Return all **10-letter sequences that occur more than once** in `s` (overlapping occurrences count), each listed once, in dictionary order.

For `"AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"` the answer is `["AAAAACCCCC", "CCCCCAAAAA"]`.

The starter code counts every sequence by scanning the whole string. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
repeated_dna('AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT')
```

Output:

```text
['AAAAACCCCC', 'CCCCCAAAAA']
```

**Example 2**

Input:

```python
repeated_dna('AAAAAAAAAAAAA')
```

Output:

```text
['AAAAAAAAAA']
```

### Constraints

- `0 <= len(s) <= 100000`
- `s` contains only `A`, `C`, `G`, `T`.

## Explanation

`seen` holds all windows met so far; `repeated` the ones met again.

### Complexity

- Time: O(n). Every window is 10 letters (a constant), so there are `n - 9` windows, each hashed once.
- Space: O(n). The sets of seen windows.
