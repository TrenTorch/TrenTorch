---
name: sheet-isomorphic-strings
title: 'Isomorphic Strings'
tags: [dsa-sheet, hashing, counting-with-dictionaries]
difficulty: Intermediate
---

## Statement

Two strings of the same length are **isomorphic** if you can replace each letter of `s` with another letter to get `t`, so that: the same letter always becomes the same letter, and **different letters never become the same letter** (no two letters map to one). A letter may map to itself. Strings of different lengths are never isomorphic.

### Examples

**Example 1**

Input:

```python
isomorphic_strings('egg', 'add')
```

Output:

```text
True
```

`e -> a`, `g -> d`.

**Example 2**

Input:

```python
isomorphic_strings('foo', 'bar')
```

Output:

```text
False
```

`o` would need to become both `a` and `r`.

### Constraints

- `0 <= len(s), len(t) <= 3 * 10**5`
- Both strings contain lower-case letters.

## Theory

You need a **one-to-one mapping** (a bijection) between the letters. Checking only that `s -> t` is consistent is not enough: `"ab"` and `"aa"` would pass (`a -> a`, `b -> a`), yet two different letters map to the same one.

Check both directions. Keep a dictionary `forward` from each letter of `s` to the letter of `t`, and `backward` from each letter of `t` to the letter of `s`. For each position, a letter that already has a mapping must keep it, in both dictionaries. Any conflict means the strings are not isomorphic.

A shortcut: two strings are isomorphic exactly when they have the same **pattern**. Replacing every letter by the position where it first appeared gives the same sequence for both.

## Explanation

The loop zips both strings. `forward.setdefault(a, b)` stores the first mapping and returns the stored one afterwards; if it differs from `b`, the mapping is inconsistent. The same check on `backward` stops two letters from mapping to one.
