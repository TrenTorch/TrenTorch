---
name: sheet-gray-code
title: 'Gray Code'
tags: [dsa-sheet, recursion, recursive-thinking]
difficulty: Intermediate
theory: building-a-list-from-a-smaller-list
---

## Statement

A **Gray code** is a sequence of all `2^n` numbers from `0` to `2^n - 1` where **each number differs from the next in exactly one bit**, and the last differs from the first in one bit too. Return the standard (reflected) Gray code that starts at `0`.

For `n = 2`: `[0, 1, 3, 2]` (binary `00, 01, 11, 10`).

### Examples

**Example 1**

Input:

```python
gray_code(2)
```

Output:

```text
[0, 1, 3, 2]
```

**Example 2**

Input:

```python
gray_code(0)
```

Output:

```text
[0]
```

### Constraints

- `0 <= n <= 16`

## Explanation

`[i ^ (i >> 1) for i in range(2**n)]` builds the reflected Gray code directly. The recursive construction doubles the list at each step: `codes + [c | (1 << (k - 1)) for c in reversed(codes)]`.

### Complexity

- Time: O(2^n). Each of the `2^n` codes is `i ^ (i >> 1)`, a constant-time formula.
- Space: O(2^n). The output list.
