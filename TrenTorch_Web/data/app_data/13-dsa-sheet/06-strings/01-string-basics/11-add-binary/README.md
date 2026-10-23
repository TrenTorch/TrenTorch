---
name: sheet-add-binary
title: 'Add Binary Strings'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
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

## Theory

In Python you could convert with `int(a, 2) + int(b, 2)` and format the result with `bin(...)[2:]`, which works because Python integers are unlimited. But converting a long string into an integer has a limit for decimal digits only, not for base 2, so this is fine here.

The **by-hand** method is the one to know for languages without big integers: add digit by digit from the **right**, keeping a **carry**. At each position the sum is `digit_a + digit_b + carry`; the output digit is `sum % 2` and the new carry is `sum // 2`. Continue while either string has digits left or the carry is `1`, then reverse the collected digits.

Both versions are `O(n)`.

## Explanation

The loop walks from the last digits of both strings (using `0` when a string is shorter), adds them with the carry, appends `sum % 2` and keeps `sum // 2` as the next carry. The digits were collected right to left, so reverse them at the end.
