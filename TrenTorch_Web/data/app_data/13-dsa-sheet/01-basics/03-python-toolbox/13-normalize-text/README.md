---
name: sheet-normalize-text
title: 'Normalize Text'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Beginner
---

## Statement

Clean up `s` like this:

1. Make every letter lower case.
2. Treat every character that is not a letter (`a-z`) or a digit (`0-9`) as a separator.
3. Join the pieces with single spaces, with no space at the start or end.

Example: `"  Hello,   World!! 42 "` becomes `"hello world 42"`.

### Examples

**Example 1**

Input:

```python
normalize_text('  Hello,   World!! 42 ')
```

Output:

```text
'hello world 42'
```

**Example 2**

Input:

```python
normalize_text('---')
```

Output:

```text
''
```

### Constraints

- `0 <= len(s) <= 10**6`
- `s` contains only printable ASCII characters.

## Theory

Python's string methods do most of this work. `s.lower()` lower-cases. `s.split()` with no argument splits on any run of whitespace and drops empty pieces, and `" ".join(pieces)` glues them back with single spaces. Together `" ".join(s.split())` collapses spaces.

To turn other characters into separators, either replace them one by one (`str.translate`, or a comprehension like `c if c.isalnum() else " "`) or use a regular expression: `re.sub(r"[^a-z0-9]+", " ", s)`. Strings are immutable, so building one by `+=` in a loop is `O(n²)` for long strings; build a list and `join` it once instead.

## Explanation

Lower-case first, then `re.sub(r"[^a-z0-9]+", " ", text)` replaces every run of non-alphanumeric characters with one space, and `.strip()` removes the space at either end. For an empty or all-punctuation string the result is `""`.
