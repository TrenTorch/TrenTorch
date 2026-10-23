---
name: sheet-repeated-dna-sequences
title: 'Repeated DNA Sequences'
tags: [dsa-sheet, advanced-strings, hashing-and-structure]
difficulty: Intermediate
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

## Theory

Slide a window of 10 letters along the string. A **set** of the windows seen so far tells in `O(10)` whether the current window was seen before: if yes, record it. Windows are hashed as strings here (10 letters is short); for longer windows use a **rolling hash**, or encode the window in 2 bits per letter (an integer of 20 bits) so it is cheap to compare and to update: `code = ((code << 2) | letter) & mask`.

One pass, `O(n)`. The recorded sequences go into a set (a sequence seen three times is reported once) and are sorted at the end.

## Explanation

`seen` holds all windows met so far; `repeated` the ones met again.
