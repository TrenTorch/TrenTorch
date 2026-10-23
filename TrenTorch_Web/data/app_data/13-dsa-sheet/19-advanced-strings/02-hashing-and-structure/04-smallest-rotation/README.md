---
name: sheet-smallest-rotation
title: 'Lexicographically Smallest Rotation'
tags: [dsa-sheet, advanced-strings, hashing-and-structure]
difficulty: Advanced
---

## Statement

A **rotation** moves some letters from the front of `s` to the back (`"abcd"` can become `"cdab"`). Return the **smallest rotation in dictionary order**.

For `"bca"` the answer is `"abc"`; for `"cabcab"` it is `"abcabc"`.

### Examples

**Example 1**

Input:

```python
smallest_rotation('bca')
```

Output:

```text
'abc'
```

**Example 2**

Input:

```python
smallest_rotation('cabcab')
```

Output:

```text
'abcabc'
```

### Constraints

- `0 <= len(s) <= 200000`
- Lower-case letters.

## Theory

Comparing all `n` rotations costs `O(n²)`. A linear method keeps two candidate start positions `i` and `j` and a length `k` of how many letters they agree on. Compare `s2[i + k]` and `s2[j + k]` (where `s2 = s + s`):

- equal: `k += 1`;
- `s2[i + k] > s2[j + k]`: every start in `i .. i + k` is worse than the corresponding start after `j`, so skip them: `i += k + 1`;
- otherwise skip `j .. j + k`: `j += k + 1`.

After a skip make sure `i != j` and restart `k = 0`. When one candidate reaches `n` the other is the answer. `O(n)`.

## Explanation

`i` and `j` are the two best candidates; the one that loses a comparison skips ahead past every start it makes worse.
