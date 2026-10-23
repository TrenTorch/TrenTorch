---
name: sheet-is-rotation
title: 'Is It a Rotation?'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
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

## Theory

Trying every rotation costs `O(n²)`. There is a one-line trick: **every rotation of `s` appears inside `s + s`**. For `"abcde"`, `s + s = "abcdeabcde"` contains `"cdeab"` (starting at index 2), `"deabc"` (index 3), and so on.

So `goal` is a rotation of `s` exactly when the lengths are equal and `goal in s + s`. The length check matters: `"ab"` is inside `"abab"`... and so is `"aba"`, which is not a rotation of `"ab"`.

Python's `in` for strings is fast (it uses an optimised search), so this is practically linear.

## Explanation

Different lengths can never be rotations. For equal lengths, `s + s` contains every rotation as a substring, so a single `in` test decides it. Two empty strings are rotations of each other.
