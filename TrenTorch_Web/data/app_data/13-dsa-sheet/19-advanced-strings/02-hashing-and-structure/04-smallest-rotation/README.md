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

**Explanation:** Rotating 'bca' produces 'bca', 'cab', and 'abc'. Among these, 'abc' is alphabetically first.

**Example 2**

Input:

```python
smallest_rotation('cabcab')
```

Output:

```text
'abcabc'
```

**Explanation:** Rotating 'cabcab' gives 'cabcab', 'abcabc', 'bcabca', and repeats. The smallest lexicographically is 'abcabc'.

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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line               | Variables                            |
| ----------------------------- | ------------------------------------ |
| `n = len(s)`                  | `n = 3`                              |
| `i, j, k = 0, 1, 0`           | `s2 = 'bcabca', i = 0, j = 1, k = 0` |
| `a, b = s2[i + k], s2[j + k]` | `a = 'b', b = 'c'`                   |
| `a, b = s2[i + k], s2[j + k]` | `j = 2, b = 'a'`                     |
| `i += k + 1`                  | `i = 1`                              |
| `i += k + 1`                  | `i = 2, a = 'c'`                     |
| `j += 1`                      | `j = 3`                              |
| `return`                      | `returned = 'abc'`                   |

### Complexity

- Time: O(n), length of s.
- Extra space: O(n) extra memory for doubled string.
- The brute force takes O(n^2), quadratic over string length.
