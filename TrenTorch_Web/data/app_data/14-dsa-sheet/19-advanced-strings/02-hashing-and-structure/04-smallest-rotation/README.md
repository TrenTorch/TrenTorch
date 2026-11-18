---
name: sheet-smallest-rotation
title: 'Lexicographically Smallest Rotation'
tags: [dsa-sheet, advanced-strings, hashing-and-structure]
difficulty: Advanced
theory: two-candidates-racing
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

## Explanation

`i` and `j` are the two best candidates; the one that loses a comparison skips ahead past every start it makes worse.

### Complexity

- Time: O(n). Two candidate starts race forward; whenever they differ the loser skips past the letters it has just compared, so the pointers advance at most `2n` times.
- Space: O(n). The doubled string.
