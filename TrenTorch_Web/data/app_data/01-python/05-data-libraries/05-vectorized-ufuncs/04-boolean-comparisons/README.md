---
name: numpy-boolean-comparisons
title: Boolean Comparisons and Combining Conditions
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions using comparison operators and combined boolean conditions on arrays, and understand why Python's own `and`/`or`/`not` keywords cannot be used here.

## Theory

Comparison operators (`>`, `<`, `>=`, `<=`, `==`, `!=`) applied to an array produce a new boolean array, element-wise.

```python
arr = np.array([5, 12, 3, 18])
arr > 10     # [False, True, False, True]
```

**Combining conditions requires `&` (and), `|` (or), and `~` (not) — not Python's `and`/`or`/`not`.** Python's keywords operate on a single truth value; an array with more than one element has no single unambiguous truth value, so using them raises an error.

```python
(arr > 10) & (arr < 15)     # correct — element-wise AND
(arr > 10) and (arr < 15)    # raises an error
```

`&`, `|`, `~` are themselves ufuncs. Parentheses around each individual condition are required — `&` binds more tightly than comparison operators, so omitting them produces wrong grouping, not an error.

## Explanation

`in_range_mask` returns `(arr > low) & (arr < high)`. `outside_range_mask` returns `(arr < low) | (arr > high)`. `not_matching` returns `~(arr == value)`. Every comparison is parenthesized individually before combining, which is what makes the grouping correct given `&`/`|`'s tighter binding.
