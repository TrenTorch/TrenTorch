---
name: sheet-normalize-text
title: 'Normalize Text'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Beginner
theory: cleaning-up-text
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

- `0 <= len(s) <= 3 * 10**5`
- `s` contains only printable ASCII characters.

## Explanation

Lower-case first, then `re.sub(r"[^a-z0-9]+", " ", text)` replaces every run of non-alphanumeric characters with one space, and `.strip()` removes the space at either end. For an empty or all-punctuation string the result is `""`.

### Complexity

- Time: O(n). Lower-casing and the regular expression each scan the string once.
- Space: O(n). The lower-cased copy and the result.
