---
name: sheet-regular-expression-matching
title: 'Regular Expression Matching'
tags: [dsa-sheet, dynamic-programming, strings-dp]
difficulty: Mastery
---

## Statement

The pattern `p` may contain `.` (matches **any single character**) and `*` (matches **zero or more copies of the character just before it**). Return `True` if `p` matches the **whole** string `s`. A `*` always follows a letter or `.`.

For `s = "aab"` and `p = "c*a*b"` the answer is `True`; for `s = "mississippi"` and `p = "mis*is*p*."` it is `False`.

### Examples

**Example 1**

Input:

```python
is_match_regex('aab', 'c*a*b')
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_match_regex('mississippi', 'mis*is*p*.')
```

Output:

```text
False
```

### Constraints

- `0 <= len(s) <= 1000`
- `0 <= len(p) <= 1000`
- `s` has lower-case letters; `p` has lower-case letters, `.` and `*`, and every `*` has a letter or `.` before it.

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

The star is now tied to the previous character, so treat `x*` as one unit. **State:** `match(i, j)`, whether `s[:i]` matches `p[:j]`. **Transition**, looking at the last pattern character:

- a letter or `.`: `match(i, j) = match(i - 1, j - 1)` when it fits `s[i - 1]`;
- `x*` (the last two pattern characters): use it **zero times** (`match(i, j - 2)`), or use it **once more** when `x` fits `s[i - 1]` (`match(i - 1, j)`: the star stays available for more copies).

**Base cases:** `match(0, 0) = True`; `match(0, j)` can be true for patterns like `a*b*` that can match nothing. `O(len(s) × len(p))`.

## Explanation

`fits(x, ch)` is `x == "." or x == ch`. In the star case, `cur[j - 2]` is "zero copies" and `prev[j]` is "one more copy".
