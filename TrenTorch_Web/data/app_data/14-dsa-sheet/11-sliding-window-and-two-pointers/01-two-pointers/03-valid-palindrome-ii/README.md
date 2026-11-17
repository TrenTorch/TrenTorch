---
name: sheet-valid-palindrome-ii
title: 'Palindrome After Deleting One Character'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Intermediate
theory: palindrome-with-one-deletion
---

## Statement

Return `True` if `s` can become a **palindrome** (reads the same both ways) by deleting **at most one** character. `"abca"` works (delete `c` or `b`); `"abc"` does not.

### Examples

**Example 1**

Input:

```python
valid_palindrome_ii('aba')
```

Output:

```text
True
```

**Example 2**

Input:

```python
valid_palindrome_ii('abca')
```

Output:

```text
True
```

### Constraints

- `0 <= len(s) <= 200000`
- Lower-case letters.

## Explanation

`is_pal(i, j)` is the plain check. At the first mismatch, one of the two characters is dropped and the rest must match completely.

### Complexity

- Time: O(n). One pass from both ends; at the first mismatch two more linear checks.
- Space: O(1). A few indices.
