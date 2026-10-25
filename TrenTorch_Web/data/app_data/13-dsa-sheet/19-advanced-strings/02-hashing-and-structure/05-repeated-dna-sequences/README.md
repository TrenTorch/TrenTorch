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

**Explanation:** The string contains two distinct 10-letter substrings that each appear at least twice, giving the output list of those substrings in alphabetical order.

**Example 2**

Input:

```python
repeated_dna('AAAAAAAAAAAAA')
```

Output:

```text
['AAAAAAAAAA']
```

**Explanation:** Every 10-letter window in the all-A string is identical, so the single repeated substring "AAAAAAAAAA" is returned.

### Constraints

- `0 <= len(s) <= 100000`
- `s` contains only `A`, `C`, `G`, `T`.

## Theory

Slide a window of 10 letters along the string. A **set** of the windows seen so far tells in `O(10)` whether the current window was seen before: if yes, record it. Windows are hashed as strings here (10 letters is short); for longer windows use a **rolling hash**, or encode the window in 2 bits per letter (an integer of 20 bits) so it is cheap to compare and to update: `code = ((code << 2) | letter) & mask`.

One pass, `O(n)`. The recorded sequences go into a set (a sequence seen three times is reported once) and are sorted at the end.

## Explanation

`seen` holds all windows met so far; `repeated` the ones met again.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line               | Variables                                                                                                                     |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `seen = set()`                | `seen = set()`                                                                                                                |
| `part = s[i : i + 10]`        | `seen = {'AAAACCCCCA', 'AAAAACCCCC'}, repeated = set(), i = 2, part = 'AAACCCCCAA'`                                           |
| `part = s[i : i + 10]`        | `seen = {'AACCCCCAAA', 'AAAAACCCCC', 'AAAACCCCCA', 'ACCCCCAAAA', ..., i = 5, part = 'CCCCCAAAAA'`                             |
| `for i in range(len(s) - 9):` | `seen = {'AACCCCCAAA', 'AAAAACCCCC', 'AAAACCCCCA', 'CCAAAAACCC', ..., i = 9, part = 'CCAAAAACCC'`                             |
| `for i in range(len(s) - 9):` | `seen = {'AACCCCCAAA', 'AAAAACCCCC', 'CAAAAACCCC', 'AAAACCCCCA', ..., repeated = {'AAAAACCCCC'}, i = 12, part = 'AAAACCCCCC'` |
| `seen.add(part)`              | `seen = {'CCCCCCAAAA', 'AACCCCCAAA', 'AAAAACCCCC', 'CAAAAACCCC', ..., i = 15, part = 'CCCCCCAAAA'`                            |
| `part = s[i : i + 10]`        | `repeated = {'CCCCCAAAAA', 'AAAAACCCCC'}, i = 19, part = 'CCAAAAAGGG'`                                                        |
| `return`                      | `returned = ['AAAAACCCCC', 'CCCCCAAAAA']`                                                                                     |

### Complexity

- Time: O(n) where n is length of s.
- Extra space: O(n) extra memory for the seen and repeated sets.
- The brute force takes O(n) where n is length of s.
