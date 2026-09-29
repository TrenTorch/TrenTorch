---
name: python-strings-splitting-joining
title: Splitting and Joining
tags: [python-strings]
difficulty: Intermediate
---

## Statement

Implement functions that break text into pieces and reassemble it, including the difference between splitting on whitespace and splitting on an explicit separator.

## Theory

`s.split()` with no argument splits on runs of whitespace and discards empty pieces:

```python
"  a   b\tc\n".split()        # ["a", "b", "c"]
```

`s.split(sep)` with an explicit separator splits at every occurrence of `sep` and **keeps** empty pieces:

```python
"a,,b,".split(",")            # ["a", "", "b", ""]
```

An optional second argument `maxsplit` limits the number of splits: `"a,b,c,d".split(",", 1)` gives `["a", "b,c,d"]`. `rsplit` counts splits from the right: `"a,b,c,d".rsplit(",", 1)` gives `["a,b,c", "d"]`. If the separator doesn't occur at all, both return a single-element list containing the whole string, regardless of `maxsplit`.

`s.splitlines()` splits at line boundaries. Unlike `split("\n")`, it does not produce a trailing empty piece for a final newline.

**Joining.** `sep.join(pieces)` builds one string from an iterable of strings, placing `sep` between them — the method is called on the **separator**. `join` computes the total length first and copies each piece once, which is why it's the recommended way to build a string from many pieces (see the Concatenation topic).

**Where this matters later.** `split` and `join` are the standard tools for parsing text records and assembling output.

## Explanation

`last_field` calls `line.rsplit(sep, 1)[-1]` unconditionally rather than checking "does `sep` occur" first — when `sep` is absent, `rsplit` with any `maxsplit` still returns a single-element list containing the whole line, so `[-1]` already gives `line` back with no separate branch needed. `count_nonblank_lines` checks `line.strip() != ""` per line from `splitlines()` (not `line != ""`), so a line containing only spaces is correctly treated as blank rather than counted.
