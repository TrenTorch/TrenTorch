---
name: python-strings-comparison-bytes
title: 'Comparison & Bytes'
tags: [python-strings, comparison, encoding]
difficulty: Intermediate
---

## Statement

Implement lexicographic comparison by hand using character codes, a case-preserving letter-shifting function and functions that convert between text and bytes, measuring how many bytes a string needs and verifying round trips.

## Theory

### Membership, comparison, & ordering

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

**Where this matters later.** Character codes are the bridge to the Text vs bytes section below: text becomes numbers, and the numbers become bytes.

### Text vs bytes

A `str` is a sequence of **characters** (code points). Computers store and transmit **bytes**: integers from `0` to `255`. An **encoding** maps each character to one or more bytes; **decoding** is the reverse.

```python
data = "Hi".encode("utf-8")     # b'Hi'
data[0]                         # 72       an int, not a string
list(data)                      # [72, 105]
data.decode("utf-8")            # "Hi"
```

**UTF-8** uses a variable number of bytes per character:

| Code point range        | Bytes per character |
| ----------------------- | ------------------- |
| U+0000, U+007F (ASCII) | 1                   |
| U+0080, U+07FF         | 2                   |
| U+0800, U+FFFF         | 3                   |
| U+10000 and above       | 4                   |

The important consequence: **`len(s)` counts characters, while `len(s.encode("utf-8"))` counts bytes**, and the two are equal only when every character is ASCII.

Decoding bytes with the wrong encoding, or bytes not valid in the chosen encoding, produces `UnicodeDecodeError`. Both `encode` and `decode` accept an `errors` argument: `"strict"` (default, raises), `"replace"` (substitutes a placeholder) and `"ignore"` (drops the offending data).

```python
"café".encode("ascii", errors="ignore")      # b'caf'
```

**Where this matters later.** Byte-level tokenizers used by language models start from exactly this representation: text is encoded to UTF-8, and each resulting integer is a basic token before larger tokens are learned.

## Explanation

`compare_strings` deliberately loops over `ord()` of each position rather than delegating to `<`/`==` on the whole strings (per the exercise's own constraint), so the code makes the "compare first differing character, else compare lengths" rule explicit rather than trusting it to the built-in operator. `caesar_shift` branches on `'a' <= ch <= 'z'` vs `'A' <= ch <= 'Z'` to pick the right base letter for the modular shift, leaving anything outside both ranges (digits, punctuation, non-ASCII) untouched, exactly the "letters only" scope the theory specifies.

`is_ascii_only` compares `len(s)` against `len(s.encode("utf-8"))` rather than looping over characters checking `ord(ch) < 128`, the theory's own consequence ("the two lengths are equal only when every character is ASCII") is a direct, O(1)-per-character test that needs no explicit per-character branch. `roundtrip` passes `errors="replace"` only on the encode step; by the time decoding runs, the bytes already came from a successful (possibly lossy) encode of that same encoding, so they're guaranteed valid to decode without needing `errors="replace"` again.
