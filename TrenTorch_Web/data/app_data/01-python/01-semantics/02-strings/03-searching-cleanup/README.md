---
name: python-strings-searching-cleanup
title: 'Case, Search & Cleanup'
tags: [python-strings, searching]
difficulty: Intermediate
---

## Statement

Implement functions that convert and inspect letter case, locate substrings and classify characters and clean the edges of a string while substituting text, avoiding the common misunderstanding of what `strip` actually removes.

## Theory

### Case methods

String methods are functions attached to the `str` type, called with dot syntax. Because strings are immutable, every method below returns a new string.

| Method           | Result                                                                           |
| ---------------- | -------------------------------------------------------------------------------- |
| `s.upper()`      | Every letter converted to uppercase.                                             |
| `s.lower()`      | Every letter converted to lowercase.                                             |
| `s.title()`      | The first letter of each run of letters uppercase, the rest lowercase.           |
| `s.capitalize()` | The first character uppercase, **all other characters lowercase**.               |
| `s.swapcase()`   | Uppercase letters become lowercase and lowercase become uppercase.               |
| `s.casefold()`   | An aggressive lowercase form intended for comparing text without regard to case. |

Two behaviors that catch people out:

- `capitalize()` lowercases everything after the first character: `"pyTHON".capitalize()` is `"Python"`.
- `title()` treats any non-letter character as a word boundary, including an apostrophe: `"they're".title()` is `"They'Re"`.

**`casefold()` vs `lower()`.** Some characters have no one-to-one lowercase form, the German `"ß"` lowercases to `"ß"` but casefolds to `"ss"`. To compare two strings ignoring case, apply `casefold()` to both and compare the results.

**Case tests** return `bool` and never change the string: `isupper()`, `islower()`, `istitle()`. `isupper()` is `True` only if the string contains at least one letter and every letter is uppercase, digits and punctuation are ignored and `"123".isupper()` is `False`.

**Where this matters later.** Normalizing text is the first step of most text pipelines, including tokenizers that feed language models.

### Searching & checking content

**Locating a substring.**

| Method                 | Behavior                                                   |
| ---------------------- | ---------------------------------------------------------- |
| `s.find(sub)`          | Index of the first occurrence of `sub`, or `-1` if absent. |
| `s.rfind(sub)`         | Index of the last occurrence, or `-1`.                     |
| `s.count(sub)`         | Number of **non-overlapping** occurrences.                 |
| `s.startswith(prefix)` | `True` if `s` begins with `prefix`.                        |
| `s.endswith(suffix)`   | `True` if `s` ends with `suffix`.                          |
| `sub in s`             | `True` if `sub` occurs anywhere in `s`.                    |

`find`, `rfind`, and `count` accept optional `start` and `end` arguments that limit the search to the slice `s[start:end]`.

```python
s = "banana"
s.find("an")        # 1
s.find("an", 2)     # 3      search from index 2 onward
s.count("an")       # 2
s.count("ana")      # 1      matches do not overlap: "ana" at 1 uses index 3
```

**The `-1` trap.** `find` returns `-1` for "not found," but `-1` is also a valid negative index. Using the result directly as an index, as in `s[s.find("x")]`, silently reads the last character. Always test the result against `-1` first, or use `in` when only presence matters.

**The empty string** is a substring of every string: `"" in "abc"` is `True`, and `"abc".find("")` is `0`.

**Character-class checks** return `bool` and test the entire string, returning `False` for the empty string: `isdigit()`, `isalpha()`, `isalnum()`, `isspace()`.

**Where this matters later.** Search-and-scan loops using `find` with a moving `start` are the manual form of what tokenizers do when matching patterns in text.

### Trimming & replacing

**Trimming.** `strip`, `lstrip`, and `rstrip` return a new string with characters removed from the ends. With no argument they remove whitespace. With a string argument, that string is treated as a **set of individual characters**, and any of those characters are removed from the end(s) until a character not in the set is reached, the argument is **not** a prefix or suffix removed as a unit.

```python
"  hi  ".strip()              # "hi"
"xxhixx".strip("x")           # "hi"
"abcabxyz".lstrip("abc")      # "xyz"   removes a, b, c, a, b one at a time
```

To remove an exact prefix or suffix once, use `removeprefix()` and `removesuffix()`:

```python
"abcabxyz".removeprefix("abc")    # "abxyz"
"file.txt".removesuffix(".txt")   # "file"
```

**Replacing.** `s.replace(old, new)` returns a new string with **every** non-overlapping occurrence of `old` replaced by `new`. An optional third argument limits how many replacements are made, starting from the left. A negative limit means "no limit."

```python
"a-b-c-d".replace("-", "+")       # "a+b+c+d"
"a-b-c-d".replace("-", "+", 2)    # "a+b+c-d"
```

**Where this matters later.** Cleaning inputs at their edges is routine when loading text datasets and parsing configuration values. The set-of-characters meaning of `strip` is a frequent source of silent data bugs.

## Explanation

`sentence_case` combines `s[0].upper()` with `s[1:].lower()` rather than `s.capitalize()` directly, so the exercise actually practices the slicing-plus-case-method combination the theory describes, even though `capitalize()` alone would give the same result. `case_kind` checks the three case tests in the fixed order the spec requires (`isupper`, `islower`, `istitle`) so an all-uppercase single-letter string (which satisfies more than one test simultaneously in edge cases) resolves predictably rather than by accident.

`find_all` advances its search position by exactly 1 after each hit (`start = idx + 1`), not by `len(sub)`, advancing by the match length is what `count()`'s non-overlapping behavior effectively does, and this question exists specifically to demonstrate the overlapping alternative. `has_extension` builds the exact suffix `"." + ext` and lower-cases both sides before comparing, so a bare `"pdf"` (no dot) correctly fails even though it contains the extension text.

`clean_field` runs `strip()`, then `rstrip(".,;")`, then `strip()` again, exactly as the three numbered steps specify, the second `strip()` matters because removing trailing punctuation can expose more trailing whitespace underneath it (e.g. `"total ;"` becomes `"total "` after the punctuation strip, still needing one more whitespace trim). `remove_prefix_once` uses `startswith` plus a single slice rather than `lstrip(prefix)`, since `lstrip` treats its argument as a character set and would strip repeated occurrences of any of those characters, not one exact prefix.
