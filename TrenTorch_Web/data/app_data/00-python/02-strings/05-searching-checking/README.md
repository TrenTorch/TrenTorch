---
name: python-strings-searching-checking
title: Searching and Checking Content
tags: [python-strings, searching]
difficulty: Intermediate
---

## Statement

Implement functions that locate substrings, count occurrences, test prefixes and suffixes, and classify strings by the kinds of characters they contain.

## Theory

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

## Explanation

`find_all` advances its search position by exactly 1 after each hit (`start = idx + 1`), not by `len(sub)` — advancing by the match length is what `count()`'s non-overlapping behavior effectively does, and this question exists specifically to demonstrate the overlapping alternative. `has_extension` builds the exact suffix `"." + ext` and lower-cases both sides before comparing, so a bare `"pdf"` (no dot) correctly fails even though it contains the extension text.
