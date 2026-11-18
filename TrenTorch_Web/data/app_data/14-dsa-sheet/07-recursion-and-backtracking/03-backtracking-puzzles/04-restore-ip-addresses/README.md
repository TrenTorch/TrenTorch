---
name: sheet-restore-ip-addresses
title: 'Restore IP Addresses'
tags: [dsa-sheet, recursion, backtracking-puzzles]
difficulty: Intermediate
theory: cutting-a-string-into-valid-pieces
---

## Statement

`s` is a string of digits. Return every **valid IP address** you can make by inserting three dots into `s` (without removing or reordering digits), sorted as strings. A valid address has **four parts**, each a number from `0` to `255` with **no leading zero** (the single digit `"0"` is fine, `"01"` is not).

For `"25525511135"`: `255.255.11.135` and `255.255.111.35`.

### Examples

**Example 1**

Input:

```python
restore_ip_addresses('25525511135')
```

Output:

```text
['255.255.11.135', '255.255.111.35']
```

**Example 2**

Input:

```python
restore_ip_addresses('0000')
```

Output:

```text
['0.0.0.0']
```

### Constraints

- `0 <= len(s) <= 14`
- `s` contains only digits.

## Explanation

With four parts the whole string must be used (`start == len(s)`). For fewer parts, every length from 1 to 3 is tried; a part is valid when it does not start with `0` (unless it is exactly `"0"`) and is at most `255`. The final list is sorted.

### Complexity

- Time: O(1). At most 3 choices for each of 4 parts, so 81 branches; the string has at most 12 digits.
- Space: O(1). The output has at most a few dozen addresses.
