---
name: python-strings-trimming-replacing
title: Trimming and Replacing
tags: [python-strings]
difficulty: Intermediate
---

## Statement

Implement functions that clean the edges of a string and substitute text, avoiding the common misunderstanding of what `strip` actually removes.

## Theory

**Trimming.** `strip`, `lstrip`, and `rstrip` return a new string with characters removed from the ends. With no argument they remove whitespace. With a string argument, that string is treated as a **set of individual characters**, and any of those characters are removed from the end(s) until a character not in the set is reached — the argument is **not** a prefix or suffix removed as a unit.

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

`clean_field` runs `strip()`, then `rstrip(".,;")`, then `strip()` again, exactly as the three numbered steps specify — the second `strip()` matters because removing trailing punctuation can expose more trailing whitespace underneath it (e.g. `"total ;"` becomes `"total "` after the punctuation strip, still needing one more whitespace trim). `remove_prefix_once` uses `startswith` plus a single slice rather than `lstrip(prefix)`, since `lstrip` treats its argument as a character set and would strip repeated occurrences of any of those characters, not one exact prefix.
