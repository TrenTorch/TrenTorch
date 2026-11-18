---
name: sheet-add-binary
title: 'Add Binary Strings'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
theory: adding-with-a-carry
---

## Statement

`a` and `b` are non-negative numbers written in **binary** as strings of `0` and `1` (with no leading zeros, except for the number zero itself, written `"0"`). Return their sum, also in binary, with no leading zeros.

### Examples

**Example 1**

Input:

```python
add_binary('11', '1')
```

Output:

```text
'100'
```

**Example 2**

Input:

```python
add_binary('1010', '1011')
```

Output:

```text
'10101'
```

### Constraints

- `1 <= len(a), len(b) <= 10**5`
- Both strings contain only `0` and `1`.

## Explanation

The loop walks from the last digits of both strings (using `0` when a string is shorter), adds them with the carry, appends `sum % 2` and keeps `sum // 2` as the next carry. The digits were collected right to left, so reverse them at the end.

### Complexity

- Time: O(max(n, m)). One pass over the digits from the right.
- Space: O(max(n, m)). The result digits.
