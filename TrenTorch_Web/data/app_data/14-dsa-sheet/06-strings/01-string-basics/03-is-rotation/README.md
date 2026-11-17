---
name: sheet-is-rotation
title: 'Is It a Rotation?'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
theory: the-doubling-trick
---

## Statement

A **rotation** moves some characters from the front of a string to its back, keeping their order (`"abcde"` rotated by 2 is `"cdeab"`). Return `True` if `goal` can be obtained from `s` by some number of rotations (zero counts).

### Examples

**Example 1**

Input:

```python
is_rotation('abcde', 'cdeab')
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_rotation('abcde', 'abced')
```

Output:

```text
False
```

### Constraints

- `0 <= len(s), len(goal) <= 3 * 10**5`
- Both strings contain lower-case letters.

## Explanation

Different lengths can never be rotations. For equal lengths, `s + s` contains every rotation as a substring, so a single `in` test decides it. Two empty strings are rotations of each other.

### Complexity

- Time: O(n). A rotation of `s` is a substring of `s + s`; CPython 3.10+ searches substrings in linear time.
- Space: O(n). The doubled string.
