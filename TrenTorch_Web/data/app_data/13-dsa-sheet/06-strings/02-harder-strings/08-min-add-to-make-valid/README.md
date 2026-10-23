---
name: sheet-min-add-to-make-valid
title: 'Minimum Insertions to Balance Parentheses'
tags: [dsa-sheet, strings, harder-strings]
difficulty: Intermediate
---

## Statement

`s` contains only `(` and `)` and may be unbalanced. You may insert parentheses anywhere. Return the **minimum number of insertions** needed to make `s` a valid balanced string, where every `(` has a matching `)` after it.

### Examples

**Example 1**

Input:

```python
min_add_to_make_valid('())')
```

Output:

```text
1
```

Insert one `(` at the start.

**Example 2**

Input:

```python
min_add_to_make_valid('(((')
```

Output:

```text
3
```

Insert three `)`.

### Constraints

- `0 <= len(s) <= 3 * 10**5`
- `s` contains only `(` and `)`.

## Theory

You do not need a stack; a counter of **currently open** parentheses is enough. Scan left to right with `open_count`:

- A `(` increases `open_count`: it is waiting for a partner.
- A `)` with `open_count > 0` is matched: decrease it.
- A `)` with `open_count == 0` has nothing to match: it is **unmatched**, and you must insert one `(` for it. Count it.

At the end, `open_count` is the number of `(` still waiting, and each needs an inserted `)`. The answer is `unmatched + open_count`. One pass, `O(1)` memory.

## Explanation

`need` counts `)` that had no `(` before them (each needs an inserted `(`), and `open_count` ends as the number of `(` left unmatched (each needs an inserted `)`). Their sum is the minimum number of insertions.
