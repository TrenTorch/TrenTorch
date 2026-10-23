---
name: sheet-interleaving-string
title: 'Interleaving String'
tags: [dsa-sheet, dynamic-programming, strings-dp]
difficulty: Advanced
---

## Statement

`c` is an **interleaving** of `a` and `b` if its characters can be split into two subsequences, one spelling `a` and the other spelling `b`, using every character of `c` exactly once. Return `True` if `c` is an interleaving of `a` and `b`.

For `a = "aabcc"`, `b = "dbbca"` and `c = "aadbbcbcac"` the answer is `True`.

### Examples

**Example 1**

Input:

```python
is_interleave('aabcc', 'dbbca', 'aadbbcbcac')
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_interleave('aabcc', 'dbbca', 'aadbbbaccc')
```

Output:

```text
False
```

### Constraints

- `0 <= len(a), len(b) <= 500`
- `0 <= len(c) <= 1000`
- Lower-case letters.

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** `ok(i, j)`, whether the first `i` characters of `a` and the first `j` of `b` can interleave into the first `i + j` characters of `c`. **Transition:** the last character `c[i + j - 1]` came from `a` (then `a[i - 1]` must equal it and `ok(i - 1, j)` must hold) or from `b` (the same with `ok(i, j - 1)`). **Base case:** `ok(0, 0) = True`. If `len(a) + len(b) != len(c)` the answer is `False`.

A table of `(len(a) + 1) × (len(b) + 1)` booleans; it can be kept as one row. `O(len(a) × len(b))`.

## Explanation

`row[j]` means `ok(i, j)` for the current `i`. The first column and the first row are filled with simple checks.
