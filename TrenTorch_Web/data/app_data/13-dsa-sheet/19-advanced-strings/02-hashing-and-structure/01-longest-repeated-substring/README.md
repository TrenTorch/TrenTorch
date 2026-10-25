---
name: sheet-longest-repeated-substring
title: 'Longest Repeated Substring'
tags: [dsa-sheet, advanced-strings, hashing-and-structure]
difficulty: Mastery
---

## Statement

Return the length of the **longest substring that occurs at least twice** in `s` (the two occurrences may overlap). Return `0` if every letter occurs once.

For `"banana"` the answer is `3` (`"ana"`).

The starter code builds every substring of every length. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
longest_repeated_length('banana')
```

Output:

```text
3
```

**Explanation:** The string "banana" contains the substring "ana" twice, so the longest repeated substring has length 3.

**Example 2**

Input:

```python
longest_repeated_length('abcd')
```

Output:

```text
0
```

**Explanation:** In "abcd", no character repeats, so no substring of length >0 appears twice; answer is 0.

### Constraints

- `0 <= len(s) <= 20000`
- Lower-case letters.

## Theory

If a substring of length `L` occurs twice, so does every shorter substring inside it. So "is there a repeated substring of length `L`?" is **monotone** in `L`, and you can **binary search** the answer.

The check for one `L` must be fast. Comparing all substrings of length `L` costs `O(n × L)`; a **rolling hash** makes each window's hash an `O(1)` update: `hash(s[i + 1 : i + L + 1]) = (hash(s[i : i + L]) - s[i] × B^(L-1)) × B + s[i + L]` (modulo a large prime). Put the hashes in a set; a repeated hash means a repeated substring (with a tiny chance of a false positive, which a large modulus makes negligible).

Total `O(n log n)`. The same idea, **Rabin–Karp**, also searches a pattern in a text by comparing hashes.

## Explanation

`check(length)` slides a window and keeps the hash of each window in a set. The binary search keeps the largest length for which a repeat exists.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line               | Variables                                                                   |
| ----------------------------- | --------------------------------------------------------------------------- |
| `n = len(s)`                  | `n = 6`                                                                     |
| `mod = (1 << 61) - 1`         | `mod = 2305843009213693951`                                                 |
| `codes = [ord(c) for c in s]` | `base = 911382323, codes = [98, 97, 110, 97, 110, 97]`                      |
| `def has_repeat(length):`     | `has_repeat = <function longest_repeated_length.<locals>.has_repeat at ...` |
| `mid = (lo + hi + 1) // 2`    | `lo = 0, hi = 5, mid = 3`                                                   |
| `lo = mid`                    | `lo = 3`                                                                    |
| `hi = mid - 1`                | `hi = 3, mid = 4`                                                           |
| `return`                      | `returned = 3`                                                              |

### Complexity

- Time: O(n log n), n is length of s.
- Extra space: O(n), n is length of s.
- The brute force takes O(n^3), n is length of s.
