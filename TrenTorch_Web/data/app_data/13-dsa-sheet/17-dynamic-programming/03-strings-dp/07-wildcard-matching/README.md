---
name: sheet-wildcard-matching
title: 'Wildcard Matching'
tags: [dsa-sheet, dynamic-programming, strings-dp]
difficulty: Advanced
---

## Statement

The pattern `p` may contain `?` (matches **any single character**) and `*` (matches **any sequence of characters**, including an empty one). Return `True` if `p` matches the **whole** string `s`.

For `s = "aa"` and `p = "*"` the answer is `True`; for `s = "cb"` and `p = "?a"` it is `False`.

The starter code tries every length for every star. It is correct but too slow with many stars.

### Examples

**Example 1**

Input:

```python
is_match_wildcard('aa', '*')
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_match_wildcard('cb', '?a')
```

Output:

```text
False
```

### Constraints

- `0 <= len(s), len(p) <= 1000`
- `s` has lower-case letters; `p` has lower-case letters, `?` and `*`.

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** `match(i, j)`, whether `s[:i]` matches `p[:j]`. **Transition:** for the last pattern character `p[j - 1]`:

- a letter or `?`: `match(i, j) = match(i - 1, j - 1)` and (`p[j - 1] == '?'` or equal to `s[i - 1]`);
- a `*`: it matches nothing (`match(i, j - 1)`) or swallows one more character (`match(i - 1, j)`).

**Base cases:** `match(0, 0) = True`; `match(0, j)` is true only if `p[:j]` is all stars. A row-by-row table: `O(len(s) × len(p))`. A greedy two-pointer solution exists too, but the table is easier to get right.

## Explanation

`prev` is the row for `i - 1` and `cur` for `i`. The star case combines "empty match" (`cur[j - 1]`) and "one more character" (`prev[j]`).
