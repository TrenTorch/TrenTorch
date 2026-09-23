---
name: python-strings-membership-comparison
title: Membership, Comparison, and Ordering
tags: [python-strings, comparison]
difficulty: Intermediate
---

## Statement

Implement lexicographic comparison by hand using character codes, and a case-preserving letter-shifting function.

## Theory

**Membership.** `sub in s` is `True` when `sub` occurs as a contiguous substring of `s`.

**Character codes.** Every character has an integer code point. `ord(ch)` returns the code point of a one-character string, and `chr(n)` returns the character for a code point.

```python
ord("a")     # 97
ord("A")     # 65
chr(98)      # "b"
```

Letters occupy consecutive code points: `"a"` to `"z"` is 97 to 122, `"A"` to `"Z"` is 65 to 90.

**Comparison.** `<`, `<=`, `>`, `>=`, `==`, `!=` compare strings **lexicographically by code point**: compare the first characters' code points; if they differ, that decides the result; if equal, compare the next pair; if one string is a prefix of the other, the shorter string is smaller.

```python
"apple" < "banana"     # True    "a" (97) < "b" (98)
"Zebra" < "apple"      # True    "Z" (90) < "a" (97): uppercase sorts first
"10" < "9"             # True    "1" (49) < "9" (57): text, not numbers
"app" < "apple"        # True    prefix is smaller
```

This differs from human alphabetical order: uppercase letters sort before all lowercase letters, and digits compare as characters, not numbers. For case-insensitive ordering, compare the `casefold()` forms.

**Modular arithmetic for letter shifts.** Shifting a lowercase letter forward by `k` positions with wrap-around uses:

$$\text{new} = \big((\text{ord}(c) - \text{ord}(\texttt{"a"}) + k) \bmod 26\big) + \text{ord}(\texttt{"a"})$$

**Where this matters later.** Character codes are the bridge to the next topic: text becomes numbers, and the numbers become bytes.

## Explanation

`compare_strings` deliberately loops over `ord()` of each position rather than delegating to `<`/`==` on the whole strings (per the exercise's own constraint), so the code makes the "compare first differing character, else compare lengths" rule explicit rather than trusting it to the built-in operator. `caesar_shift` branches on `'a' <= ch <= 'z'` vs `'A' <= ch <= 'Z'` to pick the right base letter for the modular shift, leaving anything outside both ranges (digits, punctuation, non-ASCII) untouched — exactly the "letters only" scope the theory specifies.
