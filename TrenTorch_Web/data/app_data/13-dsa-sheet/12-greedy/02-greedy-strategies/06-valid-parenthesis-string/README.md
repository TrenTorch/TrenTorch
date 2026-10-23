---
name: sheet-valid-parenthesis-string
title: 'Valid Parenthesis String With Wildcards'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Advanced
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

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

Without stars you only track `open`, the number of unclosed `(`. With stars `open` becomes a **range** `[lo, hi]` of possible values: `lo` if the stars were used as `)` or empty as much as possible, `hi` if used as `(`.

- `(`: both `lo` and `hi` increase by 1.
- `)`: both decrease by 1.
- `*`: `lo` decreases by 1 (as `)`), `hi` increases by 1 (as `(`).

Keep `lo >= 0` (a negative `lo` just means that choice is not used; we can always pick empty instead). If `hi` goes **below zero**, even the most optimistic choice has too many `)`: return `False`. At the end the string is valid if `lo == 0` is possible, that is `lo == 0` after clamping.

The whole check is `O(n)` with two counters.

## Explanation

`lo` is clamped to 0 after every step; `hi < 0` means there is no way to match a `)`. At the end `lo == 0` means some choice of stars closes everything.
