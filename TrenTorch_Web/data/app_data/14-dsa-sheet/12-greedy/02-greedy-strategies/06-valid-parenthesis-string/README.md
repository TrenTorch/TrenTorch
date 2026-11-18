---
name: sheet-valid-parenthesis-string
title: 'Valid Parenthesis String With Wildcards'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Advanced
theory: parentheses-with-wildcards
---

## Statement

`s` contains `(`, `)` and `*`. Each `*` can be **a `(`, a `)` or an empty string**. Return `True` if the stars can be chosen so that the brackets are valid (every `(` closed by a later `)`, never closing more than was opened).

For `"(*)"` and `"(*))"` the answer is `True`; for `")("` it is `False`.

### Examples

**Example 1**

Input:

```python
check_valid_string('(*)')
```

Output:

```text
True
```

**Example 2**

Input:

```python
check_valid_string('(*))')
```

Output:

```text
True
```

**Example 3**

Input:

```python
check_valid_string(')(')
```

Output:

```text
False
```

### Constraints

- `0 <= len(s) <= 200000`
- Characters are `(`, `)` and `*`.

## Explanation

`lo` is clamped to 0 after every step; `hi < 0` means there is no way to match a `)`. At the end `lo == 0` means some choice of stars closes everything.

### Complexity

- Time: O(n). One pass tracking the lowest and highest possible number of open brackets.
- Space: O(1). Two counters.
