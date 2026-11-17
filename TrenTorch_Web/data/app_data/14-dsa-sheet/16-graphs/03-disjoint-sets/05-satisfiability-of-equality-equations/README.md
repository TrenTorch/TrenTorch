---
name: sheet-satisfiability-of-equality-equations
title: 'Equality Equations'
tags: [dsa-sheet, graphs, disjoint-sets]
difficulty: Intermediate
theory: grouping-by-a-rule
---

## Statement

Each string in `equations` has the form `"a==b"` or `"a!=b"`, where `a` and `b` are single lower-case letters (variables). Return `True` if you can give each variable an integer so that **all equations hold**.

For `["a==b", "b!=a"]` the answer is `False`; for `["a==b", "b==c", "a==c"]` it is `True`.

### Examples

**Example 1**

Input:

```python
equations_possible(['a==b', 'b!=a'])
```

Output:

```text
False
```

**Example 2**

Input:

```python
equations_possible(['a==b', 'b==c', 'a==c'])
```

Output:

```text
True
```

### Constraints

- `0 <= len(equations) <= 100000`
- Each equation is 4 characters: a letter, `==` or `!=`, a letter.

## Explanation

`ord(ch) - 97` maps a letter to a position in `parent`. The two loops do the unions and then the checks.

### Complexity

- Time: O(m). One union-find pass over the `m` equations on at most 26 letters.
- Space: O(1). A parent array of 26 entries.
