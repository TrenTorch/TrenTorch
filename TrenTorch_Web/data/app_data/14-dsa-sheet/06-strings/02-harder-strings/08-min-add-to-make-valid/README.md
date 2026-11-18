---
name: sheet-min-add-to-make-valid
title: 'Minimum Insertions to Balance Parentheses'
tags: [dsa-sheet, strings, harder-strings]
difficulty: Intermediate
theory: when-the-counter-cannot-go-below-zero
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

## Explanation

`need` counts `)` that had no `(` before them (each needs an inserted `(`), and `open_count` ends as the number of `(` left unmatched (each needs an inserted `)`). Their sum is the minimum number of insertions.

### Complexity

- Time: O(n). One pass counting unmatched parentheses.
- Space: O(1). Two counters.
