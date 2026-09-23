---
name: python-strings-case-methods
title: Case Methods
tags: [python-strings]
difficulty: Beginner
---

## Statement

Implement functions that convert and inspect letter case using the built-in case methods.

## Theory

String methods are functions attached to the `str` type, called with dot syntax. Because strings are immutable, every method below returns a new string.

| Method | Result |
|---|---|
| `s.upper()` | Every letter converted to uppercase. |
| `s.lower()` | Every letter converted to lowercase. |
| `s.title()` | The first letter of each run of letters uppercase, the rest lowercase. |
| `s.capitalize()` | The first character uppercase, **all other characters lowercase**. |
| `s.swapcase()` | Uppercase letters become lowercase and lowercase become uppercase. |
| `s.casefold()` | An aggressive lowercase form intended for comparing text without regard to case. |

Two behaviors that catch people out:

- `capitalize()` lowercases everything after the first character: `"pyTHON".capitalize()` is `"Python"`.
- `title()` treats any non-letter character as a word boundary, including an apostrophe: `"they're".title()` is `"They'Re"`.

**`casefold()` vs `lower()`.** Some characters have no one-to-one lowercase form — the German `"ß"` lowercases to `"ß"` but casefolds to `"ss"`. To compare two strings ignoring case, apply `casefold()` to both and compare the results.

**Case tests** return `bool` and never change the string: `isupper()`, `islower()`, `istitle()`. `isupper()` is `True` only if the string contains at least one letter and every letter is uppercase — digits and punctuation are ignored, and `"123".isupper()` is `False`.

**Where this matters later.** Normalizing text is the first step of most text pipelines, including tokenizers that feed language models.

## Explanation

`sentence_case` combines `s[0].upper()` with `s[1:].lower()` rather than `s.capitalize()` directly, so the exercise actually practices the slicing-plus-case-method combination the theory describes, even though `capitalize()` alone would give the same result. `case_kind` checks the three case tests in the fixed order the spec requires (`isupper`, `islower`, `istitle`) so an all-uppercase single-letter string (which satisfies more than one test simultaneously in edge cases) resolves predictably rather than by accident.
